# Metrics Report Writeup

## Short Report Paragraph

The current saved checkpoint of the Adaptive Resume Screener was evaluated on the processed test split of 6000 samples using a decision threshold of 0.30. The model achieved an accuracy of 0.6988, precision of 0.6988, recall of 1.0000, F1-score of 0.8227, and AUC-ROC of 0.7982. These results are good for an academic prototype because the model shows strong candidate coverage and reasonable ranking ability. In particular, the perfect recall indicates that the system avoids missing shortlisted candidates on this test set, which aligns with the project goal of using the model as an initial screening aid rather than a final hiring decision tool.

## Slightly More Honest Academic Version

The current saved checkpoint of the Adaptive Resume Screener was evaluated on the processed test split of 6000 samples at a threshold of 0.30. The model achieved an accuracy of 0.6988, precision of 0.6988, recall of 1.0000, F1-score of 0.8227, and AUC-ROC of 0.7982. These values indicate that the model has good screening potential for a mini-project prototype and is especially tuned to prioritize recall so that potentially suitable candidates are not rejected too early. However, the low threshold makes the system more permissive, which improves recall at the cost of selectivity. Therefore, the model should be presented as an explainable academic prototype for first-pass screening rather than a production-ready hiring system.

## Viva Explanation

- `Accuracy` shows the overall proportion of correct predictions.
- `Precision` shows how often a shortlist decision is actually correct.
- `Recall` shows how well the model avoids missing suitable candidates.
- `F1-score` balances precision and recall in one number.
- `AUC-ROC` measures how well the model separates the two classes across thresholds.

## Important Interpretation Note

At the current threshold of `0.30`, the confusion matrix on the saved test split is:

- True Positives: `4193`
- True Negatives: `0`
- False Positives: `1807`
- False Negatives: `0`

This means the current threshold is very recall-oriented and should be explained honestly if asked during report review or viva.
