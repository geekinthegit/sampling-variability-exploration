# Statistical Exploration

These notes document my personal exploration of statistical concepts using data from my earlier [coding-manual-ablation](https://github.com/geekinthegit/coding-manual-ablation) study.

I begin by asking what I want to know. I decide what to change and what to hold constant, then observe the results. Finally, I examine what I learned and what remains unknown.

This project does not change the original study's prespecified analysis plan or results. All additional analyses are separate exploratory learning activities.

## Experiment Roadmap

The experiments are arranged so that concepts learned in earlier steps can be applied in later ones.

| No. | Experiment Question | Concepts | New API Calls |
| --- | --- | --- | --- |
| 01 | Why do exact agreement and Cohen's κ change differently? | Observed agreement, expected agreement, Cohen's κ | None |
| 02 | How do predictions for the same utterance change across conditions? | Paired data, label transitions, classification errors | None |
| 03 | What distribution of estimates produces a bootstrap confidence interval? | Bootstrap distribution, confidence interval | None |
| 04 | How do estimates and confidence interval widths change with sample size? | Sampling variability, precision, sample size | None |
| 05 | How much do results change when the same 300 utterances are tested again? | Model response variability, repeatability | 5,400 initial calls plus tie-breaking |
| 06 | Are results similar in new samples? What happens with larger samples? | Replication, sampling variability, precision planning | Depends on sample size |

### 01. Accuracy and Cohen's κ

Calculate observed agreement ($P_o$) and expected agreement ($P_e$) from the original confusion matrices. Explore hypothetical changes in category proportions. Examine what exact agreement alone does not capture.

### 02. Paired label transitions

Compare the baseline labels and replacement-condition labels for the same 300 utterances. Count how many labels changed. Distinguish cases that changed from agreement to disagreement with human labels from cases that changed in the opposite direction. Understand why pairs must be preserved at the utterance level.

### 03. Bootstrap distribution

Plot the distribution of paired-bootstrap replicate estimates from the original 300 utterances. Examine how the confidence interval endpoints are calculated. If the replicate estimates were not preserved, recompute them from the original final labels. No API calls are needed.

### 04. Sample size and precision

Repeatedly draw subsets of 50, 100, 150, 200, and 250 utterances from the original 300. Compare Δκ and bootstrap confidence intervals across subsets. Examine how estimates vary and how interval widths change with n. Use the full 300-utterance results as a reference.

This experiment uses only the existing 300 utterances. It does not directly observe results from new samples of 600 or 900 utterances.

### 05. Same-sample rerun

Repeat the API experiment with the same 300 utterances and conditions. Compare individual final labels, κ, and Δκ with the original results. Examine whether responses change even when the same model settings are requested.

One rerun cannot fully estimate model response variability or completely separate it from sampling variability. The execution environment and model availability must also be checked.

### 06. New-sample replication and expansion

Draw new utterances without overlapping with the original 300 and run the same procedure. Compare new samples of equal size. Then examine how Δκ and confidence intervals change when samples are combined to reach 600 or more utterances.

Whether a new Δκ falls within the original confidence interval is not a criterion for successful replication. Cumulative samples overlap and must not be treated as independent replications. The sample size will be determined after reviewing earlier experiments and the desired precision.

## Working Principles

- Do not modify the original research data or reports. Use copies or read-only access when necessary.
- Before each experiment, record the **question → what to change → what to hold constant → expected results**.
- After each experiment, record the **observations → interpretation → what remains unknown**.
- Experiments 01–04 use existing data. Before Experiments 05–06, document costs and execution rules in `PLAN.md`.
- Do not present additional findings from this repository as prespecified results of the original study.

## Learning Notes

- [01. Accuracy and Cohen's κ](01-accuracy-and-kappa.md)
