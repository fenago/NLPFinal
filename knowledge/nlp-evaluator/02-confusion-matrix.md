# 02 — Confusion matrix: computing, plotting, reading

Sources:
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ConfusionMatrixDisplay.html

Fetched: 2026-11-20 (scikit-learn 1.9.1 docs)

## confusion_matrix
`sklearn.metrics.confusion_matrix(y_true, y_pred, *, labels=None, sample_weight=None, normalize=None)`
- Definition (docs): "a confusion matrix C is such that C[i,j] is equal to the number of observations known to be in group i and predicted to be in group j." So **rows = true class, columns = predicted class**.
- `labels`: list that fixes row/column order (docs example `labels=["ant","bird","cat"]` gives `[[2,0,0],[0,0,1],[1,0,2]]`: one "bird" was predicted "cat", one "cat" was predicted "ant").
- `normalize` in `{'true','pred','all'}` (default `None`): `'true'` normalizes over rows (each true class sums to 1 -> **recall** per row on the diagonal), `'pred'` over columns (diagonal = **precision**), `'all'` over the whole population.
- Binary shortcut from docs: `tn, fp, fn, tp = confusion_matrix([0,1,0,1],[1,1,1,0]).ravel().tolist()` -> `(0, 2, 1, 1)`.

## ConfusionMatrixDisplay
`ConfusionMatrixDisplay(confusion_matrix, *, display_labels=None)` (if `display_labels` is None, labels are 0..n_classes-1). Docs example:
```python
cm = confusion_matrix(y_test, predictions, labels=clf.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
disp.plot()
plt.show()
```
- `.plot(*, include_values=True, cmap='viridis', xticks_rotation='horizontal', values_format=None, ax=None, colorbar=True, im_kw=None, text_kw=None)` returns the display object.
- Classmethod `ConfusionMatrixDisplay.from_predictions(y_true, y_pred, ...)` exists (linked on the page; its parameters such as `normalize`/`labels` were **not** in the extracted text — unverified here).

## Reading the 3-class matrix (project)
Order `labels=["neg","neu","pos"]`:

| true \ pred | neg | neu | pos |
|---|---|---|---|
| neg (1–2 stars) | correct | neg read as neutral | **neg read as positive** (sarcasm, mixed review) |
| neu (3 stars) | neutral read as neg | correct | neutral read as pos |
| pos (4–5 stars) | pos read as neg (e.g. "not bad", "sick") | pos read as neutral (short, factual) | correct |

How to read:
1. Diagonal / row sum = per-class recall; diagonal / column sum = per-class precision.
2. Look at the **biggest off-diagonal cells** first; those are the error-analysis queue (05-error-analysis.md).
3. A heavy `neu` column means VADER's +/-0.05 band is too narrow/wide for review text; a heavy `neu` row means 3-star reviews are mixed, not neutral.
4. `neg -> pos` cells are the most embarrassing (a 1-star labelled positive); count them separately.

## Code: save table + figure for the report
```python
import json, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

LABELS = ["neg", "neu", "pos"]
cm = confusion_matrix(y_true, y_pred, labels=LABELS)
cm_row = confusion_matrix(y_true, y_pred, labels=LABELS, normalize="true")   # recall view
json.dump({"labels": LABELS, "counts": cm.tolist(), "row_normalized": cm_row.round(3).tolist()},
          open("eval/vader_confusion.json", "w"), indent=2)
ConfusionMatrixDisplay(cm, display_labels=LABELS).plot(cmap="Blues", values_format="d")
plt.savefig("eval/vader_confusion.png", dpi=150, bbox_inches="tight")
```
(`values_format="d"` is a format spec for the cell values per the `values_format` parameter; `"d"` itself is a standard Python format code.)

## Project application
- Produce the matrix twice: raw counts and `normalize="true"`.
- Compare two configurations side by side: VADER on raw text vs VADER on entity-masked text (docs/02 says "Best Buy" leaks +0.64 into a factual sentence) — a shift in the `neu` row is the expected win.
- Save JSON + PNG into an `eval/` folder; do not overwrite the dashboard data.
