# ENGINE — Behind The Hug Story System
How stories go from zero to published video. No step skipped, no step out of order.

## THE LOOP
```
1. PLAN BATCH      → python3 new_batch.py --plan      (5 idea slots, avoidance rules enforced)
2. WRITE IDEAS     → fill IDEA-TEMPLATE.md for each slot (human does the creative work here)
3. REGISTER        → python3 new_batch.py --register batches/BATCH-NN.md
4. 4-STEP PIPELINE (per story, in order):
     Step 1: TITLE      → pick/optimize (CTR: number + time + emotion)
     Step 2: VOICEOVER  → full narration script, ~120 wpm, [pause] cues kept
     Step 3: OUTLINE    → scene breakdown w/ timestamps (avatar vs b-roll marked)
     Step 4: PROMPTS    → image prompt + image-to-video prompt per scene
5. PRODUCE         → avatar segments + b-roll + edit + captions + upload
6. UPDATE          → used-list auto-updates at register time; never edit counts by hand
```

## AVOIDANCE RULES (enforced by new_batch.py)
- Any component used ≥ 3× cumulative (threshold in USED-LIST.json) is BANNED for the next batch.
- Within one batch: no repeated reveal set (R1–R6), no repeated twist (T1–T5), max 2 ideas sharing a breed or branch.
- Narrator rotation: the least-used narrator gets priority.
- New components may be added to USED-LIST.json (e.g. new breed) — they start at count 0.

## BATCH SIZE
5 ideas per batch. 10-min long-form format. Twist at ~70% runtime, setback at ~55%, hook in first 18 seconds, 2-beat ending.

## FOLDER LAYOUT
```
behind-the-hug-engine/
  ENGINE.md            ← this file
  IDEA-TEMPLATE.md     ← every idea fills this
  USED-LIST.json       ← the memory; scripts only
  STRATEGY.md          ← the human's channel strategy
  new_batch.py         ← planner + registrar
  batches/
    BATCH-01-....md    ← 5 completed ideas per file
```
