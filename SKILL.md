---
name: hitl-work
description: "Human-in-the-loop multi-agent coding workflow. Use when: decompose PRD, plan, execute, QA, or review code. ID: buatin plan, kerjain sesuai plan, QA dulu, cek security, audit, debug, refactor, bikin unit test. Skip: one-liners, commit messages, snippets."
---

# HITL·Work

One agent, one job. Pipeline: `decomposer.md` → `planner.md` → `doubt-review.md` → `executor.md` → `unit-test-writer.md` → `qa.md` → specialist reviews → `documentation.md` → `skill-extractor.md`. Read the stage file before acting.

STOP gates BEFORE any agent runs. 1) Anti-slop: detect once per project (INSTALLED or NOT INSTALLED). If NOT INSTALLED with no saved preference: STOP, ask (yes / yes, always / no / never ask again), save to `.hitl-work/preferences.md`. 2) Mode: present Full / Standard / Quick with your recommendation, wait for the explicit choice, record in `status.md`; refuse unsafe picks.

Agent table, modes, routing, checkpoints, recovery, lean values: `RULES.md`.
