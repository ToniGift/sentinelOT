"""Run scenarios through the full pipeline and save a CSV.
Usage:
  python eval.py             # the 12 development scenarios
  python eval.py heldout     # the 10 held-out scenarios (run once)
"""
import csv
import sys
import time

from orchestrator import run_triage
from scenarios import technique_match

which = sys.argv[1] if len(sys.argv) > 1 else "dev"
if which == "heldout":
    from scenarios_heldout import SCENARIOS, EXPECTED, tech_ok
else:
    from scenarios import SCENARIOS, EXPECTED

    def tech_ok(got, exp):
        want = exp["techniques"]
        return technique_match(got, want) if want else not got

rows = []
for sid, alert in SCENARIOS.items():
    try:
        r = run_triage(alert)
    except Exception as e:
        print(sid, "FAILED:", e)
        rows.append({"scenario": sid, "verdict": "FAILED"})
        continue
    exp = EXPECTED[sid]
    got = [t["id"] for t in r["attack"]["techniques"]]
    rows.append({
        "scenario": sid,
        "verdict": r["triage"]["verdict"],
        "expected_verdict": exp["verdict"],
        "verdict_ok": r["triage"]["verdict"] == exp["verdict"],
        "priority": r["triage"]["priority"],
        "techniques": " ".join(got),
        "expected_techniques": " ".join(exp["techniques"]),
        "technique_ok": tech_ok(got, exp),
        "intel_items": len(r["intel"]["items"]),
        "intel_dropped": r["intel"]["dropped_unverified"],
        "invalid_ids_dropped": r["attack"]["dropped_invalid"],
        "step_failures": len(r["errors"]),
        "seconds": r["total_seconds"],
        "prompt_tokens": sum(x["prompt_tokens"] or 0 for x in r["trace"]),
        "completion_tokens": sum(x["completion_tokens"] or 0
                                 for x in r["trace"]),
    })
    print(f"{sid}: {rows[-1]['verdict']:<14} verdict_ok="
          f"{rows[-1]['verdict_ok']} technique_ok={rows[-1]['technique_ok']}"
          f" {rows[-1]['seconds']}s")

good = [r for r in rows if "verdict_ok" in r]
name = f"eval_{which}_{time.strftime('%Y%m%d_%H%M%S')}.csv"
fields = list(good[0].keys()) if good else ["scenario"]
with open(name, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
print(f"\nSet: {which}")
print(f"Verdicts matching:    {sum(r['verdict_ok'] for r in good)}/{len(rows)}")
print(f"Techniques matching:  {sum(r['technique_ok'] for r in good)}/{len(rows)}")
print(f"Saved {name}")
