# 01 — Classification metrics (scikit-learn)

Sources:
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html

Fetched: 2026-11-20 (scikit-learn 1.9.1 docs)

## accuracy_score
`sklearn.metrics.accuracy_score(y_true, y_pred, *, normalize=True, sample_weight=None)`
- Returns fraction of correct predictions (`normalize=True`) or the count (`normalize=False`). Best = 1.0.
- Example from docs: `y_true=[0,1,2,3]`, `y_pred=[0,2,1,3]` -> `0.5`; `normalize=False` -> `2.0`.
- Pitfall: accuracy hides class imbalance. Review stars are usually skewed positive; a "always positive" baseline can look good. The project samples equal 1–5 stars (docs/04) which makes neutral (3-star) only 20 % of the data, and negative (1–2) 40 %, positive (4–5) 40 %.

## precision_recall_fscore_support
`precision_recall_fscore_support(y_true, y_pred, *, beta=1.0, labels=None, pos_label=1, average=None, warn_for=(...), sample_weight=None, zero_division='warn')`
- `average`: `'micro'`, `'macro'`, `'samples'`, `'weighted'`, `'binary'` or `None` (default shown as `None` in the signature; the parameter text says default `'binary'` — for multiclass pass `average` explicitly).
  - `None` -> per-label arrays, one entry per label.
  - `'macro'` -> "Calculate metrics for each label, and find their unweighted mean" (treats all classes equally; punishes a weak neutral class).
  - `'weighted'` -> mean weighted by support (number of true instances per label); follows class frequency.
  - `'micro'` -> global counts of TP/FP/FN.
- Returns `(precision, recall, fbeta_score, support)`; `support` is the number of occurrences of each label in `y_true`, and is `None` when `average` is not None.
- `labels=[...]` sets which labels are included **and their order** in the output:
  ```python
  precision_recall_fscore_support(y_true, y_pred, average=None, labels=['pig','dog','cat'])
  # -> (array([0., 0., 0.66]), array([0., 0., 1.]), array([0., 0., 0.8]), array([2, 2, 2]))
  ```
- `zero_division`: `"warn"` (acts as 0 plus warning), `0.0`, `1.0` (and `np.nan` since 1.3 per classification_report page). Set it explicitly to avoid warnings when a class is never predicted.

## classification_report
`classification_report(y_true, y_pred, *, labels=None, target_names=None, sample_weight=None, digits=2, output_dict=False, zero_division='warn')`
- `labels`: label values to include; `target_names`: display names matching `labels` **in the same order**; `digits` default 2 (ignored with `output_dict=True`, values then unrounded); `output_dict=True` returns a dict.
- Output rows: per-class precision/recall/f1-score/support, then `accuracy`, `macro avg` (unweighted mean per label), `weighted avg` (support-weighted). Docs example:
  ```
                 precision    recall  f1-score   support
        class 0       0.50      1.00      0.67         1
        class 1       0.00      0.00      0.00         1
        class 2       1.00      0.67      0.80         3
       accuracy                           0.60         5
      macro avg       0.50      0.56      0.49         5
   weighted avg       0.70      0.60      0.61         5
  ```
- (Detail that `micro avg` replaces `accuracy` in some multilabel/subset cases is general knowledge — unverified on the page.)

## Label order matters (confusion_matrix.html)
`confusion_matrix(y_true, y_pred, *, labels=None, sample_weight=None, normalize=None)`; `C[i, j]` = number of observations known to be in group i and predicted in group j. If `labels` is omitted, labels are sorted alphabetically/numerically (standard behaviour; not in the excerpt) — so for string labels `["neg","neu","pos"]` is the default order, but **always pass `labels=` explicitly** so rows/columns match your report. Docs example: `confusion_matrix(y_true, y_pred, labels=["ant","bird","cat"])`.

## Reusable evaluation snippet
```python
from sklearn.metrics import (accuracy_score, precision_recall_fscore_support,
                             classification_report, confusion_matrix)
LABELS = ["neg", "neu", "pos"]            # fixed order everywhere

def evaluate(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    p, r, f, s = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, average=None, zero_division=0)
    macro = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, average="macro", zero_division=0)[:3]
    weighted = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, average="weighted", zero_division=0)[:3]
    return {
        "accuracy": acc,
        "per_class": {l: dict(p=p[i], r=r[i], f1=f[i], n=int(s[i])) for i, l in enumerate(LABELS)},
        "macro_f1": macro[2], "weighted_f1": weighted[2],
        "report": classification_report(y_true, y_pred, labels=LABELS, digits=3,
                                        zero_division=0, output_dict=True),
        "confusion": confusion_matrix(y_true, y_pred, labels=LABELS).tolist(),
    }
```

## Project application
- Report **macro-F1** as the headline for VADER vs stars (neutral class is hard), plus accuracy and the confusion matrix; show weighted-F1 only as a secondary number.
- Always print `support` per class so readers see the 40/20/40 split.
- Always pass `labels=["neg","neu","pos"]` and `zero_division=0`.
- Evaluate on the committed sample `data/reviews_sample.jsonl` (docs/04), with `rating` mapped 1–2 -> neg, 3 -> neu, 4–5 -> pos.
