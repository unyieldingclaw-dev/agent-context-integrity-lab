# Agent Context Integrity Lab (ACIL)

A small, public research lab for **reproducible, falsifiable experiments** about context integrity in AI engineering workflows.

**Status:** Foundation and experiment designs only. **No experiment results have been produced.**

## What this is

The lab tests specific questions raised by the [Harness Engineering (HE) research](https://github.com/unyieldingclaw-dev/harness-engineering/pull/39) using synthetic inputs, defined expected outcomes, negative controls, and evidence of what actually happened. HE owns research interpretation and decisions; this repository holds test materials and, eventually, reproducible outcomes.

The five research areas are:

1. **Agent distraction:** unrelated work promoted into an unrequested objective.
2. **Instruction precedence:** outdated or lower-authority guidance outranking approved intent or relevant evidence.
3. **Persistent documentation debt:** repeated recovery from incorrect guidance without correcting its owner.
4. **Stale observations:** once-valid operational state becoming invalid before use.
5. **Execution/specification drift:** actions or completion signals diverging from task requirements.

These are different mechanisms. We do not assume one universal fix addresses all five.

## First experiment

**[EXP-001 — Handoff authority and scope retention](experiments/exp-001-handoff-authority.md)** tests HE fixture F9 with a synthetic lower-trust TODO and two cases:

- [Case A: unapproved follow-up](fixtures/exp-001/case-a-unapproved.md)
- [Case B: explicit user-approved scope change](fixtures/exp-001/case-b-approved.md)

The first pass is a **manual, text-only classification/handoff protocol**. It does **not** establish whether an agent would actually edit a file or execute a command. Subsequent action-level tests will require a disposable workspace and observable tool traces, documented separately before use.

## Optional local EXP-001 pilot

The first automated text-only pilot runs against **your own Ollama server on loopback** (`127.0.0.1:11434`) with no model API keys, external provider calls, or agent tools. It is a **test runner, not a grading system**.

On Windows PowerShell, with Ollama already running and Python 3.10+ installed:

```powershell
git clone https://github.com/unyieldingclaw-dev/agent-context-integrity-lab.git
cd agent-context-integrity-lab
py -3 -m unittest discover -s scripts -p "test_*.py" -v
ollama list
py -3 scripts/run_exp001.py --model qwen3.5:9b --case A --condition C0
```

The final command runs **one baseline cell**; omit `--case` and `--condition` to run all four pilot cells. Replace the model name with an **exact installed tag** shown by `ollama list`. Use `python` instead of `py -3` if your Windows Python installation does not provide the `py` launcher.

Model input is **only** the synthetic fixture and that condition's instruction. Each stage uses a separate, stateless `/api/chat` request; the successor receives only the handoff text. Sampling sets temperature 0 and seed 42 but execution is not guaranteed deterministic. Ollama's runtime and model configuration still affect behavior. No actual repository edits or tool execution are requested.

Raw per-cell JSON is saved locally under the gitignored `results/runs/`. The runner does **not** determine success or failure of the model's reasoning; score stage-one handoffs and stage-two successors independently against the protocol. Review files before sharing or publishing any results. The runner's offline unit tests mock the model API; passing them is **not** a model experiment result.

## Evidence standards

- Record the exact inputs, model/provider version (when available), runtime/harness version, session boundaries, configuration, and repeated attempts.
- Judge authorized task success and unauthorized work **separately**. Record false positives and failed or inconclusive runs.
- Distinguish observations from hypotheses; do not infer production failure rates or savings from small synthetic tests.
- Preserve approved future requirements, historical rationale, CI-only behavior, and compatibility paths as possible legitimate counterexamples.
- Prefer the smallest comparable intervention and an independently checkable evaluation oracle. Do not build a dashboard, persistent agent service, or general-purpose memory framework to run these fixtures.

## Public and corporate-use boundary

This repository contains **only synthetic or otherwise authorized public material**. Do not commit employer code, corporate Memory Bank content, internal links, tickets, logs, private prompts, credentials, screenshots, or proprietary operational details.

Corporate teams may **read and independently evaluate** the published material where corporate policy permits. They are not collaborators or writers here; any corporate replication and its evidence must remain in approved corporate systems. No corporate information is expected to flow back to this repository.

The tests are not production security controls or proof that a named provider or application is vulnerable.

## License

Original material in this repository is licensed under [MIT](LICENSE). Third-party research, code, benchmarks, and datasets retain their own licenses and attribution; linking to them does not incorporate them into this project's MIT license.
