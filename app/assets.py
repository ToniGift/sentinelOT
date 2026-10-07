import json

_A = json.load(open("data/assets.json", encoding="utf-8"))


def lookup_asset(key):
    if not key:
        return {"known": False}
    for ip, v in _A.items():
        if key == ip or key == v["name"]:
            return {"known": True, "ip": ip, **v}
    return {"known": False, "id": key}
