import json
import time
from concurrent.futures import ThreadPoolExecutor

from assets import lookup_asset
from attack_ics import catalogue, load_ics
from config import MODELS
from intel import canon, is_trusted, search
from llm import call_json
from prompts import (ADVISOR_SYS, INTAKE_SYS, INTEL_SYS, MAPPER_SYS,
                     TRIAGE_SYS)
from schemas import (AdvisorResult, Indicators, IntakeResult, IntelResult,
                     MapperResult, TriageResult)

TECHS = load_ics()
CATALOGUE = catalogue(TECHS)
NAMES = {c["id"]: c["name"] for c in CATALOGUE}
ORDER = {"intake": 0, "search": 1, "intel": 2, "mapper": 3,
         "triage": 4, "advisor": 5}


def step(trace, errors, name, system, payload, schema, required=False):
    """Run one LLM agent. Records a trace row. Optional agents degrade
    gracefully (return None); required agents re-raise."""
    t0 = time.time()
    row = {"step": name, "model": MODELS[name], "prompt_tokens": None,
           "completion_tokens": None}
    try:
        out, u = call_json(MODELS[name], system,
                           json.dumps(payload, ensure_ascii=False), schema)
        row.update(status="ok",
                   prompt_tokens=getattr(u, "prompt_tokens", None),
                   completion_tokens=getattr(u, "completion_tokens", None))
        return out
    except Exception as e:
        row["status"] = "failed"
        errors.append(f"{name} failed: {e}")
        if required:
            raise
        return None
    finally:
        row["seconds"] = round(time.time() - t0, 2)
        trace.append(row)


def _search_all(queries, errors):
    """Run the (up to 3) searches in parallel, de-duplicate by URL."""
    def one(q):
        try:
            return search(q)
        except Exception as e:
            errors.append(f"search failed for '{q}': {e}")
            return []

    with ThreadPoolExecutor(max_workers=3) as ex:
        results = list(ex.map(one, queries))
    hits, seen = [], set()
    for res in results:
        for h in res:
            key = canon(h.get("url"))
            if h.get("url") and key not in seen:
                seen.add(key)
                hits.append(h)
    return hits


def _intel_branch(alert, intake, trace, errors):
    t0 = time.time()
    hits = _search_all(intake.search_queries[:3], errors)
    trace.append({"step": "search", "model": "tavily", "status": "ok",
                  "seconds": round(time.time() - t0, 2),
                  "prompt_tokens": None, "completion_tokens": None,
                  "hits": len(hits)})
    trust = {h["url"]: is_trusted(h["url"]) for h in hits}
    intel = None
    if hits:
        intel = step(trace, errors, "intel", INTEL_SYS,
                     {"alert": {"title": alert.title,
                                "description": alert.description},
                      "results": [{"title": h["title"], "url": h["url"],
                                   "content": h["content"]} for h in hits]},
                     IntelResult)
    if intel is None:
        intel = IntelResult(summary="No threat intelligence retrieved.",
                            items=[])
    kept = [i for i in intel.items if i.url in trust]          # validator
    return {"summary": intel.summary,
            "items": [{**i.model_dump(), "trusted": trust[i.url]}
                      for i in kept],
            "dropped_unverified": len(intel.items) - len(kept)}


def _mapper_branch(alert, intake, ctx, trace, errors):
    text = " ".join([alert.title, alert.description,
                     alert.protocol or "", intake.summary])
    mapped = step(trace, errors, "mapper", MAPPER_SYS,
                  {"alert": text, "assets": ctx, "catalogue": CATALOGUE},
                  MapperResult)
    techniques, ids, dropped = [], set(), 0
    for t in (mapped.techniques if mapped else []):                # validator
        if t.id in NAMES and t.id not in ids:
            ids.add(t.id)
            techniques.append({"id": t.id, "name": NAMES[t.id],
                               "rationale": t.rationale})
        elif t.id not in NAMES:
            dropped += 1
    return {"techniques": techniques, "dropped_invalid": dropped}


def run_triage(alert) -> dict:
    t_start = time.time()
    trace, errors = [], []
    ctx = {"src": lookup_asset(alert.src_asset or alert.src_ip),
           "dst": lookup_asset(alert.dst_asset or alert.dst_ip)}

    # 1 Intake
    intake = step(trace, errors, "intake", INTAKE_SYS,
                  {"alert": alert.model_dump(), "assets": ctx}, IntakeResult)
    if intake is None:
        intake = IntakeResult(summary=alert.title, indicators=Indicators(),
                              search_queries=[alert.title])

    # 2 + 3 run side by side: (search -> intel) and mapper
    with ThreadPoolExecutor(max_workers=2) as ex:
        f_intel = ex.submit(_intel_branch, alert, intake, trace, errors)
        f_map = ex.submit(_mapper_branch, alert, intake, ctx, trace, errors)
        intel_out, attack_out = f_intel.result(), f_map.result()

    # 4 Triage (required)
    triage = step(trace, errors, "triage", TRIAGE_SYS,
                  {"alert": alert.model_dump(), "assets": ctx,
                   "intake": intake.model_dump(), "intel": intel_out,
                   "attack": attack_out}, TriageResult, required=True)

    # 5 Advisor
    advice = step(trace, errors, "advisor", ADVISOR_SYS,
                  {"triage": triage.model_dump(), "assets": ctx,
                   "attack": attack_out}, AdvisorResult)
    advice_out = (advice.model_dump() if advice else
                  {"summary": "Advisor unavailable.", "actions": []})

    trace.sort(key=lambda r: ORDER[r["step"]])
    return {"alert": alert.model_dump(), "intake": intake.model_dump(),
            "intel": intel_out, "attack": attack_out,
            "triage": triage.model_dump(), "advice": advice_out,
            "trace": trace, "errors": errors,
            "total_seconds": round(time.time() - t_start, 2),   # wall clock
            "sum_step_seconds": round(sum(r["seconds"] for r in trace), 2)}
