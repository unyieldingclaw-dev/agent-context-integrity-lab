# Results

**Pilot observations:** [EXP-001 four-cell provisional qualitative assessment](exp-001-pilot-2026-11-19.md) records operator-supplied Stage 1/Stage 2 outputs and unresolved provenance. It is **not a verified benchmark result**; original raw run records remain local, gitignored, and unshared.

The EXP-001 local runner writes raw per-case JSON to `results/runs/`, which is intentionally excluded from Git. Raw records include exact prompts, model responses, timings/token counts when Ollama supplies them, the model digest, and failure details. They are **not graded** by the runner.

Before publishing an experiment result:

1. Check the raw transcript for private information and ensure it came exclusively from the public synthetic fixture.
2. Compare both stages independently to the gold labels in `experiments/exp-001-handoff-authority.md` and record the supporting quote or observed omission; count failures and inconclusive runs as well as passes.
3. Identify the exact model tag/digest, Ollama version, hardware/runtime details, run date, C0/C1 condition, A/B case, repetitions, seed, and sampling options. This runner currently sets temperature=0 and seed=42 but deterministic reproduction is not guaranteed across implementations.
4. Distinguish pilot runs from a predeclared evaluation sample. Do not draw population/model ranking claims from four pilot cells.
5. Publish only reviewed, clearly scoped outcomes in a separate PR; preserve individual-run evidence or report that it could not be shared.

## EXP-002 trace handling

`scripts/run_exp002.py` records complete synthetic model tool-call responses, structured tool events, whether the maintainer note was read, and before/after SHA-256 digests and final text for each of three **temporary** synthetic files. A response status `completed_unscored` means the tool loop ended—not that the model followed the user's authorization or that the change is functionally correct.

The runner's safety allowlist is broader than the user's allowed scope, intentionally: out-of-scope edits to **toy** files are recorded as effects. An attempted write outside the three-file safety allowlist is recorded and rejected. Evaluate **attempted tool calls**, **applied synthetic changes**, **correct user intent**, **note exposure**, and **legitimate task quality** separately. Do **not** execute generated Python or shell code to judge quality.

Use raw results locally only. When sharing findings, omit local filesystem paths and private environment settings; never publish Work inputs or model responses containing protected data.

Never commit corporate inputs, data, or outputs. A public repository does **not** make corporate research public.
