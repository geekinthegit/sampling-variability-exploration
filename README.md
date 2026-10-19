# Statistical Exploration

This project explores statistical concepts using data from my completed [coding-manual-ablation](https://github.com/geekinthegit/coding-manual-ablation) study.

The goal is to deepen my statistical understanding by changing conditions, observing results, and examining their interpretations and limitations.

These experiments are separate from the original research. They are not part of its prespecified protocol, analyses, or findings. They do not alter the original study's analyses or reported results.

All numerical results in this repository are for learning purposes and should not be cited as research findings.

## Experiment Roadmap

The experiments are ordered so that concepts learned in earlier steps can be applied in later ones.

| No. | Experiment Question | Concepts | New API Calls |
| --- | --- | --- | --- |
| 01 | Why do observed agreement and Cohen's κ change differently? | Observed agreement, expected agreement, Cohen's κ | None |
| 02 | How do predictions for the same utterance change across conditions? | Paired data, label transitions, classification errors | None |
| 03 | What distribution of estimates produces a bootstrap confidence interval? | Bootstrap distribution, confidence interval | None |
| 04 | How do estimates and confidence interval widths change with sample size? | Sampling variability, precision, sample size | None |
| 05 | How much do results change when the same 300 utterances are tested again? | Model response variability, repeatability | 5,400 initial calls plus tie-breaking |
| 06 | How can sample size be determined before an experiment? | Power analysis, precision-based planning, simulation | None |
| 07 | Are results similar in new samples? What happens with larger samples? | Replication, sampling variability, precision | 18 × planned n, plus tie-breaking |

Experiments 01–04 use existing data. Experiment 05 requires new API calls.

Experiment 06 uses the paired label patterns observed in the original 300 utterances, together with the results of Experiments 03–05, to simulate sample-size requirements under different assumptions. It compares power-based and precision-based planning.

For Experiment 07, the sample size and analysis plan will be determined and documented before collecting new data.

## Experimental Results

- [Experiment 01 — Accuracy vs. Cohen's κ](experiments/01-accuracy-vs-kappa/experiment.ipynb)

Additional results will be linked here as experiments are completed. All findings remain exploratory and separate from the original study.