# Statistics Learning Notes

이 노트는 기존 `coding-manual-ablation` 연구의 데이터를 활용해 통계 개념을 직접 실험하며 이해하기 위한 학습 기록이다. 기존 연구의 분석계획이나 결과를 변경하는 작업과는 별개로 진행한다.

## 실험 로드맵

순서는 의도적으로 정했다. 뒤의 실험이 앞에서 배운 개념을 이용하도록 구성했다.

| 순서 | 실험 질문 | 배우는 개념 | 새 API 호출 |
| --- | --- | --- | --- |
| 1 | 정확도와 κ는 왜 다르게 변할까? | Cohen's κ, 우연 일치도 | 불필요 |
| 2 | 같은 발화의 예측이 어떻게 달라졌을까? | Paired data, 분류 오류 | 불필요 |
| 3 | 표본을 다르게 뽑으면 결과가 얼마나 흔들릴까? | Sampling variability, precision | 불필요 |
| 4 | 완전히 새로운 표본에서도 결과가 유지될까? | Replication, sample size | 필요 |
| 5 | 같은 표본을 다시 모델에 넣으면 결과가 같을까? | Model variability, reliability | 필요 |

## 학습 노트

- [01. Accuracy and Cohen's κ](../notes/01-accuracy-and-kappa.md)
