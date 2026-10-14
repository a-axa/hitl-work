# HITL·Work — Structured Vibe Coding

Vibe coding is fast. It's also how you ship bugs, lose context between sessions, and end up with code nobody can audit — including yourself.

HITL·Work keeps the speed. It adds structure.

17 agents. Each with one job. The Planner never writes code. The Executor never improvises. QA never approves without reading the actual code. Every decision lands in a file. Every session picks up exactly where the last one ended.

---

## What you get

**Speed without chaos.** You still move fast — the pipeline removes friction, not velocity. Planner writes the spec so Executor doesn't have to think. Executor follows the spec so QA doesn't have to guess.

**A paper trail by design.** Every feature produces a folder:

```
.hitl-work/features/your-feature/
  status.md          ← source of truth across sessions
  prd.md             ← the plan
  doubt-review.md    ← stress-test before execution
  test-plan.md       ← approved before test code is written
  qa-report.md       ← verdict with evidence
  reviews/           ← security, performance, migration
  TECH-DEBT.md       ← what was deferred and why
```

Six months later, you open that folder and reconstruct the full decision history — what was planned, what was questioned, what was verified, what was intentionally left for later.

**Cheap models where the work is mechanical. Strong models where it matters.** The Executor follows a spec. It doesn't need to reason about architecture — so you can run it on a smaller model. The Planner and reviewers need judgment — use a stronger one there.

**Context survives session boundaries.** `status.md` is updated at every handoff. The next session reads it and knows exactly where things stand — what's approved, what's open, what's blocked.

---

## Pipeline

```
(Decomposer) → Planner → (Doubt Review) → Executor → (Unit Test Writer) → QA → (Specialist Reviews) → Documentation
```

Three modes, picked explicitly by you before any agent runs (the agent recommends the lowest safe one and validates your choice):

| Mode | Use for |
|---|---|
| 🔴 **Full Pipeline** | New feature, migration, security surface, unclear scope |
| 🟡 **Standard** | Scoped bug fix or enhancement, 1–2 files, no high-risk surface |
| 🟢 **Quick** | Typo, config correction, isolated one-file hotfix |

Quick mode is not permitted for migrations, auth/authz, external APIs, DB queries, or anything touching more than one file. If a risk signal appears mid-execution, escalate immediately.

---

## 📦 Install as Skill

```bash
# Permanent install for this project
npx skills add "https://github.com/iskandar221201/hitl-work" --skill hitl-work

# Global install (all projects)
npx skills add "https://github.com/iskandar221201/hitl-work" --skill hitl-work -g

# One-shot without installing
npx skills use "https://github.com/iskandar221201/hitl-work" --skill hitl-work
```

```bash
npx skills list       # verify project-level
npx skills list -g    # verify global
```

Triggers automatically on: `plan this feature`, `decompose PRD`, `buat prd`, `execute prd.md`, `QA`, `doubt review`, `security review`, `architecture review`, `debug`, `refactor`, `API design`, `unit test` — including Indonesian equivalents (`buatin fitur`, `kerjain sesuai prd`, `cek security`, `bikin unit test`).

Does not trigger for: commit messages, one-liners, `cat file`, SQL one-offs, translations.

---

## 🤝 Pairs well with: anti-slop

HITL·Work gives your agents structure. [anti-slop](https://github.com/miqdadbadjuber/anti-slop) gives their output taste: it filters generic AI-generated code, UI, and copy.

The pairing is opt-in and handled automatically. On the first run in a project, HITL·Work checks whether the anti-slop skill is installed:

- **Installed** → the QA and Documentation agents read its rules and add an explicit slop check to their verdicts.
- **Not installed** → the agent stops and asks you first (`yes` / `yes, always` / `no` / `never ask again`). Nothing is ever installed silently, and your answer is saved (`.hitl-work/preferences.md` per project, `~/.hitl-work/preferences.md` global) so you are only asked once.

Install it manually any time:

```bash
npx skills add miqdadbadjuber/anti-slop
```

---

## Agents

### Core Pipeline

| Agent | File | Role |
|---|---|---|
| 🧩 **Decomposer** | `decomposer.md` | Breaks a large PRD into discrete `task-N.md` files by domain boundary. Does not plan, does not execute. Stops for human review before passing to Planner. |
| 🧠 **Planner** | `planner.md` | Produces `prd.md` — a complete, unambiguous spec covering necessity check (YAGNI+DRY), security, performance, observability, testability, and UI/UX. Does not write code. |
| 🔍 **Doubt Review** | `doubt-review.md` | Adversarial spec reviewer. Finds hidden assumptions, scope creep, and missing edge cases before execution. Cheap to run; expensive to skip. |
| ⚙️ **Executor** | `executor.md` | Implements `prd.md` step by step. Stops and asks on ambiguity. Never improvises. |
| 🧪 **Unit Test Writer** | `unit-test-writer.md` | Reads the spec, produces a Test Plan (human-approved), then generates test code for the detected stack. Sits between Executor and QA. |
| 🔍 **QA** | `qa.md` | Verifies implementation against spec — compliance, breaking changes, Definition of Done, code quality. Records evidence. Issues PASS / FAIL / PASS WITH WARNINGS. Writes TECH-DEBT.md for anything intentionally deferred. |

### Specialist Reviews

Run after Executor. Report findings only — never fix.

| Agent | File | Focus |
|---|---|---|
| 🏛️ **Architecture Review** | `architecture-review.md` | Layer boundaries, dependency direction, duplication vs. reuse |
| 🔒 **Security Review** | `security-review.md` | Auth/authz, input validation, data exposure, secrets |
| ⚡ **Performance Review** | `performance-review.md` | N+1, indexing, caching, memory, scalability |
| 🗄️ **Migration Review** | `migration-review.md` | Migration safety, rollback, locking risk, data integrity |
| ♻️ **Refactor Agent** | `refactor-agent.md` | Abstraction opportunities, coupling, readability — produces a plan, not code |
| 🎨 **UI/UX Planner** | `ui-ux-planner.md` | UI spec: tokens, component reuse, loading/empty/error states |
| 🧩 **UI Skill Extractor** | `ui-skill-extractor.md` | Extracts visual patterns into a reusable skill file after QA |

### Supporting Agents

| Agent | File | Role |
|---|---|---|
| 🔌 **API Agent** | `api-agent.md` | DESIGN / INTEGRATION / AUDIT of HTTP APIs |
| 🐛 **Debug Agent** | `debug.md` | Root-cause investigation. Does not fix — produces a handoff to Executor. |
| 📚 **Skill Extractor** | `skill-extractor.md` | Distills codebase patterns into `skill.md` — read by all agents before acting |
| 📖 **Documentation** | `documentation.md` | Writes docs from what was actually built, not what was planned |

---

## Required Routing

Some changes require specific agents regardless of mode. Record skips in `status.md` with human-accepted rationale.

| Condition | Required |
|---|---|
| New endpoint, auth/authz, webhook, user-controlled input, external API | Security Review |
| Schema change, index, backfill, data migration | Doubt Review + Migration Review |
| New query, bulk operation, caching, queue/job, high-traffic endpoint | Performance Review |
| Cross-module change, new architectural pattern, substantial refactor | Architecture Review |
| New screen, critical UI flow, reusable UI component | UI/UX Planner + UI Skill Extractor after QA |
| Non-trivial business logic | Unit Test Writer including approved Test Plan |
| Bug with unknown root cause | Debug Agent before planning a fix |

---

## Re-verification Loop

Findings get IDs (`QA-001`, `SEC-001`, `PERF-001`). Executor fixes only approved findings. QA verifies the regression. Critical findings are re-checked by the specialist who reported them. A finding closes only as `Fixed`, `Accepted risk`, or `Deferred` — with the decision recorded in `status.md`.

---

## Why separate agents?

A single prompt doing everything is how you get hallucinated architecture, skipped security checks, and a QA that approves its own output. Separating the roles forces each stage to be an independent check on the previous one.

Narrow scope also means more reliable output from cheaper models. The Executor follows a spec — it doesn't need heavy reasoning. The Planner and reviewers need judgment — allocate accordingly.

Every agent can be called independently. Need only a security audit? Run Security Review. Already have a spec? Start at Executor. Already have code? Start at QA.

---

## How to use

1. Pick a mode and record it in `status.md`.
2. **Large PRD?** Decomposer first — break into `task-N.md`, review, then continue.
3. **Planner** — describe the feature. Get `prd.md`.
4. **Doubt Review** — if the spec touches anything risky.
5. **Executor** — implements per spec, one step at a time.
6. **Unit Test Writer** — for non-trivial logic: Test Plan → approval → test code.
7. **QA** — full verification with recorded evidence.
8. **Specialist reviews** — as required by routing table.
9. **Documentation + Skill Extractor** — close the loop after all findings are resolved.
