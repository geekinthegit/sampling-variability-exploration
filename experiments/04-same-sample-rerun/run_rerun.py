"""Experiment 04 wrapper: run the original runner with its output redirected here.

What this wrapper does
----------------------
* Imports ``run_experiment`` from ~/coding-manual-ablation/scripts unchanged and
  sets ``run_experiment.RUNS_DIR`` to the absolute path of
  ``experiments/04-same-sample-rerun/runs`` in this repository, then calls
  ``run_experiment.main(argv)`` with the command-line arguments passed through
  verbatim. This is the same mechanism the original repository's tests use
  (tests/test_parse.py: ``monkeypatch.setattr(rx, "RUNS_DIR", ...)``). The
  wrapper does nothing else.
* Nothing under ~/coding-manual-ablation is modified. The original repository is
  only read (scripts, samples/main_targets.csv, data/, manual/) and its git
  commit is recorded in the manifest by the original ``git_commit_hash``.
* Before calling the runner it checks that the original repository's working
  tree is clean. ``git_commit_hash`` appends ``-dirty`` otherwise, and the
  runner's resume verification (5.6.6 check 5) refuses a dirty tree.
* ``sys.dont_write_bytecode = True`` so no ``__pycache__`` is written into the
  original repository's scripts/ directory.

Output location
---------------
~/statistical-exploration/experiments/04-same-sample-rerun/runs/<run_id>/
  prompts.jsonl, manifest_passN.json, attempts_passN.jsonl, labels.csv,
  final_labels.csv (and run.lock while a pass is running).
prompts.jsonl and run.lock are git-ignored (see .gitignore); the other files
are tracked.

Fixed values (identical to the original main run, reports/main-run-record-2026-09-24.md)
---------------------------------------------------------------------------------------
run_id              rerun-2026-10-20
--input             /Users/jeobnida/coding-manual-ablation/samples/main_targets.csv
--concurrency 4  --timeout 60  --backoff-initial 2  --backoff-max 60  --failure-threshold 10
Model, request parameters (temperature 0, reasoning_effort "none",
max_completion_tokens 64, strict json_schema) and the aggregation / tie-break
rules come from the original scripts and are not set here.

Order: pass 1 -> pass 2 -> pass 3. Pass 2 and pass 3 are only needed when
final_labels.csv has tie_pending rows; the runner says "pass N not needed"
otherwise and makes no call.

Commands (run from ~/statistical-exploration, conda base, with
OPENAI_API_KEY_ABLATION set in the shell)
-----------------------------------------------------------------
Step 0 (already done, no API call): dry run that wrote prompts.jsonl and
manifest_pass1.json for pass 1.

    python experiments/04-same-sample-rerun/run_rerun.py --run-id rerun-2026-10-20 --pass 1 --input /Users/jeobnida/coding-manual-ablation/samples/main_targets.csv --concurrency 4 --timeout 60 --backoff-initial 2 --backoff-max 60 --failure-threshold 10 --dry-run

Because manifest_pass1.json now exists, pass 1 is started with --resume (the
runner refuses a fresh start when the manifest exists; 5.6.6 operational note:
"--dry-run on a clean tree, then --resume"). The five operational values may be
repeated and must then equal the manifest.

    python experiments/04-same-sample-rerun/run_rerun.py --run-id rerun-2026-10-20 --pass 1 --resume --concurrency 4 --timeout 60 --backoff-initial 2 --backoff-max 60 --failure-threshold 10
    python experiments/04-same-sample-rerun/run_rerun.py --run-id rerun-2026-10-20 --pass 2 --concurrency 4 --timeout 60 --backoff-initial 2 --backoff-max 60 --failure-threshold 10
    python experiments/04-same-sample-rerun/run_rerun.py --run-id rerun-2026-10-20 --pass 3 --concurrency 4 --timeout 60 --backoff-initial 2 --backoff-max 60 --failure-threshold 10
"""

import sys
from pathlib import Path

sys.dont_write_bytecode = True

ABLATION_ROOT = Path.home() / "coding-manual-ablation"
SCRIPTS_DIR = ABLATION_ROOT / "scripts"
RUNS_DIR = Path(__file__).resolve().parent / "runs"

sys.path.insert(0, str(SCRIPTS_DIR))

import run_experiment as rx  # noqa: E402


def main(argv: list[str]) -> int:
    commit = rx.git_commit_hash()          # runs git inside ABLATION_ROOT
    if commit.endswith("-dirty"):
        print(f"refused: {ABLATION_ROOT} working tree is dirty ({commit}); "
              "the runner records this commit and resume verification refuses a dirty tree",
              file=sys.stderr)
        return 2

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    rx.RUNS_DIR = RUNS_DIR
    return rx.main(argv)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except rx.Refused as exc:            # same reporting as run_experiment.__main__
        print(f"refused: {exc}", file=sys.stderr)
        sys.exit(2)
