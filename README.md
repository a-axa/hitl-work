# Multi-Agent Development Workflow (HITL·Work)
Most AI coding workflows collapse into one prompt doing everything. HITL·Work splits it: 17 agents, each with a single responsibility — so cheap models can do senior-engineer work.
Each .md file is an independent system prompt for a single role. One agent, one responsibility. Planner doesn't write code. Executor doesn't think about architecture. QA trusts nothing without verification.

## 📦 Install as Skill

### Via `npx skills` (recommended)

```bash
# Install permanent ke project (recommended)
npx skills add "https://github.com/iskandar221201/hitl-work" --skill hitl-work

# Install global (semua project)
npx skills add "https://github.com/iskandar221201/hitl-work" --skill hitl-work -g

# One-shot tanpa install (inject ke sesi ini saja)
npx skills use "https://github.com/iskandar221201/hitl-work" --skill hitl-work
```

### Verify

```bash
npx skills list          # project-level
npx skills list -g       # global
```

> Skill trigger otomatis saat prompt menyebut: `plan this feature`, `decompose PRD`, `buat prd`, `execute prd.md`, `QA`, `doubt review`, `security review`, `architecture review`, `debug`, `refactor`, `API design`, `unit test` — termasuk padanan Indonesia (`buatin fitur`, `kerjain sesuai prd`, `cek security`, `bikin unit test`) — dan tidak trigger untuk one-liner seperti `commit message`, `cat file`, atau `translate`.

---

## Main Pipeline

```
(Decomposer) → Planner → (Doubt Review) → Executor → (Unit Test Writer) → QA → (Review specialists) → Documentation
```

0. **Decomposer** *(optional, for large-scope inputs)* — if the input is a large PRD spanning many modules, break it into discrete tasks (`task-1.md`, `task-2.md`, ...) before passing to the Planner.
1. **Planner** produces a detailed, unambiguous spec (`prd.md`) — per task (if routed through Decomposer) or directly from a feature request.
2. **Doubt Review** *(optional but recommended)* — stress-tests the spec before execution. Surfaces hidden assumptions, missed edge cases, and scope creep.
3. **Executor** implements exactly per spec — no improvisation.
4. **Unit Test Writer** *(optional but recommended for non-trivial logic)* — takes the markdown spec as input, produces a Test Plan (human-approved) then generates test code. Feeds QA with a ready verification baseline.
5. **QA** verifies that the implementation matches the spec — skeptical by default. If Unit Test Writer ran, uses generated tests as part of verification.
6. Review specialists (**Architecture, Security, Performance, Migration, UI/UX**) run in parallel or after QA, depending on what the feature touches.
7. **Documentation** & **Skill Extractor** close the cycle — documenting what was built and capturing patterns for future features.

---

## Agent List

### Intake

| Agent | File | Role |
|---|---|---|
| 🧩 **Decomposer** | `decomposer.md` | First agent in the pipeline for large PRD inputs. Reads the PRD and breaks it into discrete tasks by domain/functional boundary (not implementation steps), each saved as `task-N.md` with Goal + Context fields (including inter-task dependencies). Does not plan, does not execute — purely decomposition. Always stops for human review before tasks are passed to the Planner. |

### Core Pipeline

| Agent | File | Role |
|---|---|---|
| 🧠 **Planner** | `planner.md` | Senior Software Architect. Translates a feature request (or a single `task-N.md` from the Decomposer) into a complete implementation spec (`prd.md`) — covering necessity check (YAGNI+DRY), reusability assessment, security/performance/observability/UI-UX considerations. Does not write code. |
| ⚙️ **Executor** | `executor.md` | Meticulous Implementation Engineer. Executes `prd.md` step by step, without improvisation. Stops and asks when a step is ambiguous or blocked. |
| 🧪 **Unit Test Writer** | `unit-test-writer.md` | Test engineer. Reads a markdown spec (SKILL.md, feature doc, API contract) and produces a structured Test Plan first — stops for human approval — then generates test code adapted to the detected stack (PHPUnit, Go testing, Jest, PyTest, etc.). Sits between Executor and QA; its output becomes QA's verification baseline. |
| 🔍 **QA** | `qa.md` | Quality Assurance Engineer. Verifies Executor output against the spec — spec compliance, breaking changes, Definition of Done, and baseline code quality (logic, security, side effects, consistency). If Unit Test Writer ran, uses generated tests as part of verification. |

### Pre-Execution Review

| Agent | File | Role |
|---|---|---|
| 🔍 **Doubt Review** | `doubt-review.md` | Adversarial spec reviewer. Runs after the Planner, before the Executor. Finds hidden assumptions, scope creep, irreversible steps, missing edge cases, and ambiguities — before any code is written. |

### Post-Execution Review Specialists

Run after the Executor finishes, typically in parallel with or after QA. All agents in this category **report issues only — they do not fix them**.

| Agent | File | Focus |
|---|---|---|
| 🏛️ **Architecture Review** | `architecture-review.md` | Skill file compliance, layer boundaries (Controller/Service/Model), dependency direction, duplication vs. reuse, long-term maintainability. |
| 🔒 **Security Review** | `security-review.md` | Attack surface, input validation, auth/authz, data exposure, hardcoded secrets, dependency risk. |
| ⚡ **Performance Review** | `performance-review.md` | N+1 queries, indexing, caching, memory usage, external call resilience, scalability at 10x–100x load. |
| 🗄️ **Migration Review** | `migration-review.md` | Database migration safety — operation risk classification, rollback safety, data integrity, locking risk, backward compatibility. |
| ♻️ **Refactor Agent** | `refactor-agent.md` | Identifies abstraction opportunities, readability issues, over-engineering, and coupling — without changing behavior. Produces a prioritized refactor plan, not code. |

### UI/UX Specialists

| Agent | File | Role |
|---|---|---|
| 🎨 **UI/UX Planner** | `ui-ux-planner.md` | Called by the main Planner when UI complexity is high. Produces a precise UI spec — color/spacing tokens, components to reuse, states (loading/empty/error) — so the Executor doesn't guess at visuals. |
| 🧩 **UI Skill Extractor** | `ui-skill-extractor.md` | Reads QA-approved UI implementation and extracts/updates the project's visual skill file (`skills/[project]-ui.md`) — tokens, components, anti-patterns — so future UI audits don't start from scratch. |

### Supporting Agents

| Agent | File | Role |
|---|---|---|
| 🔌 **API Agent** | `api-agent.md` | Senior API Architect with 3 modes: **DESIGN** (create new API contracts), **INTEGRATION** (spec for consuming external APIs — resilience, retry, circuit breaker), **AUDIT** (review existing APIs/integrations). |
| 🐛 **Debug Agent** | `debug.md` | Debug investigator. Finds root causes through config-vs-bug triage, execution tracing, and evidence-backed hypotheses. Does not write fixes — produces a precise handoff to the Executor. |
| 📚 **Skill Extractor** | `skill-extractor.md` | Observes existing code and distills patterns into a `skill.md` — folder structure, naming conventions, anti-patterns — read by all other agents before working in the codebase. |
| 📖 **Documentation** | `documentation.md` | Technical writer. Writes documentation (API reference, module docs, feature guides, changelog) based on what was *actually implemented*, not what was planned. |

---

## Why Separate Agents?

- **Narrow scope → more reliable output.** Models (especially cheaper ones) perform better when the instruction is "only check security" rather than "check everything at once."
- **Cheap models for Executor, stronger models for Planner/Review.** Since the Executor just follows a detailed spec, it doesn't need heavy reasoning — as long as the spec is complete.
- **Every agent can be called independently.** Just need a security audit? Call Security Review without running the full pipeline. Just have a spec? Run Unit Test Writer standalone.
- **Skill files as shared memory.** `skill-extractor.md` and `ui-skill-extractor.md` prevent each Planner/Executor from having to re-audit the codebase from scratch every time.

---

## How to Use

1. **Large PRD with many modules?** Start with the **Decomposer** — break it into `task-N.md` per domain/module, review and agree on the task list before continuing.
2. For each task (or directly, if scope is small) — start with the **Planner**, describe the feature/bug to address.
3. If the spec touches anything risky (multi-tenant, DB migration, live users) → run **Doubt Review** before proceeding to the Executor.
4. **Executor** implements per `prd.md`.
5. For non-trivial logic → run **Unit Test Writer**: pass the spec/SKILL.md, review the Test Plan, approve, then get the test code.
6. **QA** verifies — using Unit Test Writer output as baseline if available.
7. Run relevant review specialists (e.g., DB migration involved → Migration Review; new endpoint → Security + API Agent AUDIT).
8. Once everything passes → **Documentation** & **Skill Extractor** (or **UI Skill Extractor** for UI features) to close the cycle.

Each agent refuses to do work outside its scope (e.g., the Planner refuses to write code, QA refuses to approve without reading the actual code, Unit Test Writer never generates test code without an approved Test Plan) — this is intentional, so each stage remains an independent check on the previous one.
