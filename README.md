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
| 04 | How much do results change when the same 300 utterances are tested again? | Model response variability, repeatability | 5,400 initial calls plus tie-breaking |
| 05 | How can sample size be determined before an experiment? | Power analysis, precision-based planning, simulation | None |
| 06 | Are results similar in new samples? How do estimates and interval widths change with sample size? | Replication, sampling variability, precision, sample size | 18 × planned n per new sample, plus tie-breaking |

Experiments 01–03 use existing data. Experiment 04 requires new API calls on the original 300 utterances.

Experiment 05 uses the paired label patterns observed in the original 300 utterances, together with the results of Experiments 03 and 04, to simulate sample-size requirements under different assumptions. It compares power-based and precision-based planning. The number of new samples, the conditions to run, and the stopping rule for Experiment 06 are decided here and documented before any new data are collected.

Experiment 06 draws new samples of 300 utterances from the remaining sampling frame and runs them with the original procedure. Each new sample is a replication at n = 300; the pooled samples are used to examine how estimates and interval widths change with sample size, replacing a separate subsampling experiment within the original 300.

## Experimental Results

- [Experiment 01 — Accuracy vs. Cohen's κ](experiments/01-accuracy-vs-kappa/experiment.ipynb)

Additional results will be linked here as experiments are completed. All findings remain exploratory and separate from the original study.