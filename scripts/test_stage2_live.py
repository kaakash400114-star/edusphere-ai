# Stage 2 live verification: language band across KG / grade 2 / grade 8 / grade 11
import json, urllib.request, time, sys
sys.path.insert(0, r"C:\Users\user\Documents\Programming\edusphere")
from app import language

OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
BASE = "http://127.0.0.1:8100"

def http(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Content-Type": "application/json"})
    with OPENER.open(req, timeout=120) as r:
        return json.loads(r.read())

from app import language  # repo root on sys.path when run from repo
import sys
sys.path.insert(0, r"C:\Users\user\Documents\Programming\edusphere")

CASES = [
    (0,  "cbse", "Tell me why the sky is blue"),
    (2,  "cbse", "What is photosynthesis?"),
    (8,  "cbse", "Explain Newton's third law with an example"),
    (11, "cbse", "Explain SN1 vs SN2 reaction mechanisms"),
]

RES = {}
for grade, board, q in CASES:
    prof = http("POST", "/api/profile",
                {"name": f"G{grade}T", "grade": grade,
                 "character": "leo" if grade <= 5 else "nova", "board": board})
    pid = prof["pid"]
    t0 = time.time()
    chat = http("POST", "/api/chat", {"pid": pid, "message": q,
                                      "history": [], "mode": None})
    dt = round(time.time() - t0, 1)
    ans = chat.get("answer", "")
    lint = language.lint(ans, grade)
    RES[grade] = {"q": q, "lint": lint["ok"], "violations": lint["violations"],
                  "metrics": lint["metrics"], "secs": dt,
                  "head": ans[:150].replace("\n", " ")}
    print(f"--- grade {grade} ({dt}s) lint_ok={lint['ok']} "
          f"max_words={lint['metrics']['max_words']} "
          f"long_ratio={lint['metrics']['long_ratio']}")
    if lint["violations"]:
        print("   VIOLATIONS:", lint["violations"])
    print("  ", RES[grade]["head"])
    try:
        http("DELETE", f"/api/profile/{pid}")
    except Exception:
        pass

json.dump(RES, open(r"C:\Users\user\AppData\Local\Temp\es_stage2_results.json", "w"), indent=1)
print("DONE")
