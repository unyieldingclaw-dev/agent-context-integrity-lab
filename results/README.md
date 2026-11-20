# Results

**No results have been collected or published.**

The EXP-001 local runner writes raw per-case JSON to `results/runs/`, which is intentionally excluded from Git. Raw records include exact prompts, model responses, timings/token counts when Ollama supplies them, the model digest, and failure details. They are **not graded** by the runner.

Before publishing an experiment result:

1. Check the raw transcript for private information and ensure it came exclusively from the public synthetic fixture.
2. Compare both stages independently to the gold labels in `experiments/exp-001-handoff-authority.md` and record the supporting quote or observed omission; count failures and inconclusive runs as well as passes.
3. Identify the exact model tag/digest, Ollama version, hardware/runtime details, run date, C0/C1 condition, A/B case, repetitions, seed, and sampling options. This runner currently sets temperature=0 and seed=42 but deterministic reproduction is not guaranteed across implementations.
4. Distinguish pilot runs from a predeclared evaluation sample. Do not draw population/model ranking claims from four pilot cells.
5. Publish only reviewed, clearly scoped outcomes in a separate PR; preserve individual-run evidence or report that it could not be shared.

Never commit corporate inputs, data, or outputs. A public repository does **not** make corporate research public.
