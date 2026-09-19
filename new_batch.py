#!/usr/bin/env python3
"""Batch planner + registrar for the Behind The Hug story engine.
  python3 new_batch.py --plan        → prints 5 idea slots with avoidance rules applied
  python3 new_batch.py --register batches/BATCH-NN-x.md
      → scans the file's COMPONENTS lines and bumps USED-LIST.json counts
Batch files must contain lines like:  COMPONENTS: reveal=R3 anchor=C-A3 twist=T4 ending=E3 narrator=N2 breed=Labrador branch=Navy setting=shelter
"""
import json, os, re, sys, argparse
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
UL = os.path.join(HERE, "USED-LIST.json")

CATS = ["reveal", "anchor", "twist", "ending", "narrator", "breed", "branch", "setting"]

def load():
    with open(UL) as f: return json.load(f)

def save(ul):
    with open(UL, "w") as f: json.dump(ul, f, indent=2, sort_keys=True)

def banned(ul):
    th = ul.get("avoid_threshold", 3)
    return {c: {k for k, v in ul["components"][c].items() if v >= th} for c in CATS}

def plan(_args):
    ul = load(); b = banned(ul)
    print("=== BATCH PLAN — avoidance rules applied ===\n")
    for c in CATS:
        counts = ul["components"][c]
        allow = [k for k in counts if k not in b[c]]
        print(f"{c.upper():9s} BANNED: {sorted(b[c]) or '—'}")
        print(f"{'':9s} ALLOWED: {allow}\n")
    print("SLOT RULES (5 ideas):")
    print(" 1. No reveal set (R1–R6) repeats within the batch.")
    print(" 2. No twist (T1–T5) repeats within the batch.")
    print(" 3. Max 2 ideas share a breed; max 2 share a branch.")
    print(" 4. Use the least-used narrator first.")
    print(" 5. Every idea fills IDEA-TEMPLATE.md completely before Step 1 of the pipeline.")
    least = Counter(ul["components"]["narrator"]).most_common()[-1]
    print(f"  → Start batch with narrator: {least[0]} (used {least[1]}×, lowest)")

def register(args):
    ul = load()
    path = args.file
    txt = open(path, encoding="utf-8").read()
    lines = re.findall(r"COMPONENTS:\s*(.+)", txt)
    if not lines:
        print("No COMPONENTS lines found. Add one per idea, e.g.:")
        print("COMPONENTS: reveal=R3 anchor=C-A3 twist=T4 ending=E3 narrator=N2 breed=Labrador branch=Navy setting=shelter")
        sys.exit(1)
    n = 0
    for ln in lines:
        for pair in re.findall(r"(\w+)=([\w\-/ ]+?)(?=\s\w+=|$)", ln):
            cat, val = pair[0].strip(), pair[1].strip()
            if cat in ul["components"]:
                ul["components"][cat][val] = ul["components"][cat].get(val, 0) + 1
                n += 1
    ul["batches_done"] = ul.get("batches_done", 0) + 1
    import datetime
    ul["meta"]["updated"] = datetime.date.today().isoformat()
    save(ul)
    print(f"Registered {len(lines)} ideas, {n} component counts bumped. batches_done={ul['batches_done']}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--register", action="store_true")
    ap.add_argument("--file", default="")
    a = ap.parse_args()
    if a.register: register(a)
    else: plan(a)
