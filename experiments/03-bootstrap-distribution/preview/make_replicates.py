"""Regenerate the original study's bootstrap replicates and draw their distributions.

Preview for Experiment 03. No new API calls. Nothing under ~/coding-manual-ablation
is written; its label files are read in place.

The bootstrap functions of the original study (scripts/scorer.py) are imported and
called unchanged: draw_indices(300) with the original seed, then
bootstrap_replicates(), which returns every replicate value, so no wrapper is needed.

Outputs (written next to this script):
  replicates.csv            replicate, kappa_baseline, delta_kappa_<condition> x 4
  summary.csv               percentiles, mean, sd per column, with the scoring-record interval
  hist_kappa_baseline.png   baseline kappa replicates
  hist_delta_<condition>.png  one per replacement condition
  hist_delta_overlay.png    the four delta-kappa distributions in one figure
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

print(f"python: {sys.executable}")
print(f"numpy: {np.__version__}")
print(f"pandas: {pd.__version__}")

import matplotlib  # noqa: E402  (fail here, before any work, if it is missing)

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

print(f"matplotlib: {matplotlib.__version__}")

# ---------------------------------------------------------------------------
# Inputs (read-only)
# ---------------------------------------------------------------------------
ABLATION_ROOT = Path.home() / "coding-manual-ablation"
SCORING_LABELS = ABLATION_ROOT / "data" / "scoring_labels.csv"              # git-ignored: read in place, not copied
FINAL_LABELS = ABLATION_ROOT / "runs" / "main-2026-09-24" / "final_labels.csv"
SCRIPTS_DIR = ABLATION_ROOT / "scripts"
OUT_DIR = Path(__file__).resolve().parent

for path in (SCORING_LABELS, FINAL_LABELS, SCRIPTS_DIR):
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {path}")

# Importing scorer also imports openai through its dependencies; no API key is read and no call is made.
sys.dont_write_bytecode = True        # do not write __pycache__ into the original repository
sys.path.insert(0, str(SCRIPTS_DIR))
from tags import TAG_TO_CATEGORY  # noqa: E402
from scorer import (  # noqa: E402
    BOOTSTRAP_SEED, CATEGORIES, N_REPLICATES, PAIRED_CONDITIONS, Record,
    bootstrap_replicates, delta_key, draw_indices, make_table, paired, paired_baseline_key,
    standalone, standalone_key, summarize_replicates,
)

CONDITIONS = [
    "baseline",
    "definition_replacement",
    "example_replacement",
    "exclusion_rule_replacement",
    "negative_control",
    "names_only",
]
REPLACEMENTS = CONDITIONS[1:5]
assert tuple(REPLACEMENTS) == PAIRED_CONDITIONS
assert N_REPLICATES == 10_000 and BOOTSTRAP_SEED == 20260919

# Scoring record values (Section 8: standalone baseline kappa; Section 9: delta kappa)
RECORD = {
    "kappa_baseline": {"estimate": 0.6085, "lower": 0.5266, "upper": 0.6846},
    "delta_kappa_definition_replacement": {"estimate": -0.0018, "lower": -0.0384, "upper": 0.0360},
    "delta_kappa_example_replacement": {"estimate": -0.0611, "lower": -0.1047, "upper": -0.0191},
    "delta_kappa_exclusion_rule_replacement": {"estimate": -0.1062, "lower": -0.1576, "upper": -0.0556},
    "delta_kappa_negative_control": {"estimate": -0.0232, "lower": -0.0581, "upper": 0.0118},
}

# ---------------------------------------------------------------------------
# Join of the two label files: the same method as Experiment 02, Section 2.1
# (pivot final_labels to wide, map Tag -> category name, join on source_id = utterance_id).
# Category names are kept in full here because scorer's functions require them.
# ---------------------------------------------------------------------------
final_long = pd.read_csv(FINAL_LABELS)
assert set(final_long["status"]) == {"resolved"}
model = final_long.pivot(index="utterance_id", columns="condition", values="final_label")[CONDITIONS]
model.columns.name = None

human_raw = pd.read_csv(SCORING_LABELS, keep_default_na=False, na_values=[""], usecols=["source_id", "Tag"])
assert human_raw["source_id"].is_unique
human = human_raw.set_index("source_id")["Tag"].astype(int).map(TAG_TO_CATEGORY).rename("human")

labels = model.join(human, how="left").reset_index()
labels = labels[["utterance_id", "human", *CONDITIONS]].sort_values("utterance_id").reset_index(drop=True)

assert len(labels) == 300
assert labels.notna().all().all()
assert labels["utterance_id"].is_unique
for col in ["human", *CONDITIONS]:
    assert set(labels[col]) <= set(CATEGORIES), col

# The bootstrap functions take scorer.Record objects. Build them from the joined table,
# ordered by utterance_id ascending (6.2.1: the row order is part of the reproducibility
# conditions), and check that scorer.make_table builds the identical table from the
# same inputs.
table = [
    Record(utterance_id=int(row.utterance_id), human=row.human,
           labels={c: getattr(row, c) for c in CONDITIONS},
           statuses={c: "resolved" for c in CONDITIONS})
    for row in labels.itertuples(index=False)
]
reference_table = make_table(
    {int(uid): h for uid, h in zip(labels["utterance_id"], labels["human"])},
    final_long.to_dict("records"),
)
assert table == reference_table
assert [r.utterance_id for r in table] == sorted(r.utterance_id for r in table)
print(f"table: {len(table)} records, utterance_id ascending")

# ---------------------------------------------------------------------------
# Point estimates (no random numbers) and their check against the scoring record
# ---------------------------------------------------------------------------
point = {"kappa_baseline": standalone(table, "baseline").result.kappa}
for c in REPLACEMENTS:
    p = paired(table, c)
    assert p.paired_n == 300
    point[f"delta_kappa_{c}"] = p.delta_kappa
for key, est in point.items():
    assert round(est, 4) == RECORD[key]["estimate"], (key, est)
print("point estimates match the scoring record to four decimal places")

# ---------------------------------------------------------------------------
# Bootstrap: the original functions, called unchanged, with the original seed
# ---------------------------------------------------------------------------
draws = draw_indices(len(table))                 # Generator(PCG64(20260919)).integers(0, 300, size=(10000, 300))
assert draws.indices.shape == (N_REPLICATES, 300)
assert draws.seed == BOOTSTRAP_SEED
print(f"draws: shape {draws.indices.shape}, seed {draws.seed}, numpy {draws.numpy_version}")

reps = bootstrap_replicates(table, draws)        # returns every replicate value of all 18 statistics
assert reps.n_replicates == N_REPLICATES

columns = {"kappa_baseline": reps.values[standalone_key("baseline")]}
for c in REPLACEMENTS:
    columns[f"delta_kappa_{c}"] = reps.values[delta_key(c)]
    # With no missing labels every paired set is the full replicate, so the paired-set
    # baseline kappa equals the standalone baseline kappa in every replicate.
    assert reps.values[paired_baseline_key(c)] == columns["kappa_baseline"], c

for key, values in columns.items():
    assert len(values) == N_REPLICATES
    assert all(v is not None for v in values), f"{key}: undefined replicate present"

replicates = pd.DataFrame({"replicate": np.arange(1, N_REPLICATES + 1), **columns})
replicates.to_csv(OUT_DIR / "replicates.csv", index=False)

# ---------------------------------------------------------------------------
# Summary and interval check against the scoring record
# ---------------------------------------------------------------------------
rows = []
mismatches = []
for key in columns:
    values = replicates[key].to_numpy()
    p2_5, p50, p97_5 = np.percentile(values, [2.5, 50, 97.5], method="linear")
    interval = summarize_replicates(columns[key], point[key])          # the original interval function
    assert interval.withheld_reason is None and interval.undefined_count == 0
    assert interval.lower == p2_5 and interval.upper == p97_5           # same percentile computation
    rec = RECORD[key]
    row = {
        "statistic": key,
        "point_estimate": point[key],
        "mean": values.mean(),
        "sd": values.std(ddof=1),
        "p2.5": p2_5,
        "p50": p50,
        "p97.5": p97_5,
        "record_lower": rec["lower"],
        "record_upper": rec["upper"],
        "matches_record_4dp": round(p2_5, 4) == rec["lower"] and round(p97_5, 4) == rec["upper"],
    }
    rows.append(row)
    if not row["matches_record_4dp"]:
        mismatches.append(row)

summary = pd.DataFrame(rows)
summary.to_csv(OUT_DIR / "summary.csv", index=False)

print()
print(f"{'statistic':<40} {'estimate':>9} {'p2.5':>8} {'p50':>8} {'p97.5':>8} {'rec lo':>8} {'rec hi':>8}")
for r in rows:
    print(f"{r['statistic']:<40} {r['point_estimate']:>9.4f} {r['p2.5']:>8.4f} {r['p50']:>8.4f} "
          f"{r['p97.5']:>8.4f} {r['record_lower']:>8.4f} {r['record_upper']:>8.4f}")

# ---------------------------------------------------------------------------
# Histograms (no styling)
# ---------------------------------------------------------------------------
BINS = 60


def histogram(key, title, filename, zero_line):
    values = replicates[key].to_numpy()
    lo, hi = np.percentile(values, [2.5, 97.5], method="linear")
    fig, ax = plt.subplots()
    ax.hist(values, bins=BINS)
    ax.axvline(point[key], color="black", label=f"point estimate = {point[key]:.4f}")
    ax.axvline(lo, color="gray", linestyle="--", label=f"2.5th percentile = {lo:.4f}")
    ax.axvline(hi, color="gray", linestyle="--", label=f"97.5th percentile = {hi:.4f}")
    if zero_line:
        ax.axvline(0, color="red", linestyle=":", label="0")
    ax.set_title(title)
    ax.set_xlabel(key)
    ax.set_ylabel("replicates")
    ax.legend()
    fig.savefig(OUT_DIR / filename, dpi=150)
    plt.close(fig)


histogram("kappa_baseline", "baseline κ (n = 300, B = 10,000)", "hist_kappa_baseline.png", zero_line=False)
for c in REPLACEMENTS:
    histogram(f"delta_kappa_{c}", f"{c} Δκ (n = 300, B = 10,000)", f"hist_delta_{c}.png", zero_line=True)

fig, ax = plt.subplots()
for c in REPLACEMENTS:
    ax.hist(replicates[f"delta_kappa_{c}"].to_numpy(), bins=BINS, alpha=0.5, label=c)
ax.axvline(0, color="red", linestyle=":", label="0")
ax.set_title("Δκ of the four replacement conditions (n = 300, B = 10,000)")
ax.set_xlabel("delta_kappa")
ax.set_ylabel("replicates")
ax.legend()
fig.savefig(OUT_DIR / "hist_delta_overlay.png", dpi=150)
plt.close(fig)

print()
print("written:", ", ".join(sorted(p.name for p in OUT_DIR.iterdir() if p.suffix in (".csv", ".png"))))

# The record check is reported, not forced: a mismatch stops the script after all files are written.
assert not mismatches, "interval bounds differ from the scoring record: " + ", ".join(m["statistic"] for m in mismatches)
print("all 2.5/97.5 percentiles match the scoring record to four decimal places")
