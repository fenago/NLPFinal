# Citing Datasets and Software

Sources:
- https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023 and https://amazon-reviews-2023.github.io/ (BibTeX, verbatim)
- https://huggingface.co/datasets/Yelp/yelp_review_full (citation text; arXiv 1509.01626 linked from the card)
- https://www.nltk.org/ (citation request, verbatim)
- https://raw.githubusercontent.com/explosion/spaCy/master/CITATION.cff (verbatim fields)
- https://github.com/cjhutto/vaderSentiment (README, citation text and licence line)

Fetched: 2026-11-20

Rule: the entries marked "verbatim" are copied from the source. BibTeX entries marked "constructed" were assembled from the source's plain-text citation; check them against the publisher's page before the final report (not verified here).

## Amazon Reviews 2023 (verbatim BibTeX from the dataset card and site)
```bibtex
@article{hou2024bridging,
  title={Bridging Language and Items for Retrieval and Recommendation},
  author={Hou, Yupeng and Li, Jiacheng and He, Zhankui and Yan, An and Chen, Xiusi and McAuley, Julian},
  journal={arXiv preprint arXiv:2403.03952},
  year={2024}
}
```
- Plain text: Hou, Y., Li, J., He, Z., Yan, A., Chen, X., and McAuley, J. (2024). Bridging Language and Items for Retrieval and Recommendation. arXiv:2403.03952.
- Also credit the dataset: "Amazon Reviews 2023, McAuley Lab, UCSD", category used (All_Beauty), URL https://amazon-reviews-2023.github.io/, accessed 2026-11-20. The card states no licence; say "no licence stated on the dataset card".

## Yelp Review Full / Yelp dataset (Zhang et al. 2015)
Card text (verbatim): "Xiang Zhang, Junbo Zhao, Yann LeCun. Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NIPS 2015)." The card links the paper at https://arxiv.org/abs/1509.01626 and says the data is "extracted from the Yelp Dataset Challenge 2015 data". Terms: "check the official yelp-dataset-agreement" (linked on the card).
```bibtex
@inproceedings{zhang2015character,
  title     = {Character-level Convolutional Networks for Text Classification},
  author    = {Zhang, Xiang and Zhao, Junbo and LeCun, Yann},
  booktitle = {Advances in Neural Information Processing Systems 28 (NIPS 2015)},
  year      = {2015},
  url       = {https://arxiv.org/abs/1509.01626}
}
```
(constructed from the card's citation text)
- Credit line for the app footer: "Restaurant and business reviews from the Yelp Dataset Challenge 2015 via Yelp/yelp_review_full (Zhang, Zhao and LeCun, 2015). Used under the Yelp dataset agreement for educational use."
- If the Open Dataset is used instead, cite Yelp's dataset page https://business.yelp.com/data/resources/open-dataset/ (describes itself as "intended for educational use"); its own citation wording was not retrieved (unverified).

## NLTK
Site text (verbatim): "If you publish work that uses NLTK, please cite the NLTK book as follows: Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O'Reilly Media Inc."
```bibtex
@book{bird2009natural,
  title     = {Natural Language Processing with Python},
  author    = {Bird, Steven and Loper, Edward and Klein, Ewan},
  year      = {2009},
  publisher = {O'Reilly Media Inc.}
}
```
(constructed; author order follows the nltk.org citation text: Bird, Loper, Klein. Confirm against the book's title page before the final report, since other sources print Bird, Klein, Loper.)
- Also state the NLTK version used (3.10.x in this project; see `requirements.txt`) and the VADER lexicon via `nltk.sentiment.vader`.

## spaCy
Verbatim from `CITATION.cff` (`preferred-citation`, type article): message "If you use spaCy, please cite it as below."; authors Honnibal, Matthew; Montani, Ines; Van Landeghem, Sofie; Boyd, Adriane; title "spaCy: Industrial-strength Natural Language Processing in Python"; doi `10.5281/zenodo.1212303`; year 2020.
```bibtex
@software{spacy,
  title  = {spaCy: Industrial-strength Natural Language Processing in Python},
  author = {Honnibal, Matthew and Montani, Ines and Van Landeghem, Sofie and Boyd, Adriane},
  year   = {2020},
  doi    = {10.5281/zenodo.1212303}
}
```
(constructed from the CFF fields)
- Also name the model: `en_core_web_sm` 3.8.0 (from docs/expert-roster.md) with the spaCy version used.

## VADER
Verbatim from the vaderSentiment README: "Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014." The README also says the tool is "fully open-sourced under the MIT License" and appreciates attribution.
```bibtex
@inproceedings{hutto2014vader,
  title     = {VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text},
  author    = {Hutto, C. J. and Gilbert, E. E.},
  booktitle = {Eighth International Conference on Weblogs and Social Media (ICWSM-14)},
  address   = {Ann Arbor, MI},
  year      = {2014},
  month     = {June}
}
```
(constructed from the README citation text)
- NLTK ships the VADER lexicon (`vader_lexicon`) derived from this work; cite both NLTK and Hutto and Gilbert when reporting VADER scores.

## How to present citations (Google style, see 01)
- References section in the report: alphabetical by first author; one entry per item above.
- App footer: short credit line plus a link with descriptive text, for example "see [Amazon Reviews 2023 dataset card]".
- Say what you used each for in one sentence, in present tense: "VADER scores each sentence; spaCy extracts entities."
- Include access dates for web resources (2026-11-20 for these pages).

## Project application
- Files: `CITATIONS.md` (or a "Credits" section in README) holds the BibTeX above; the in-app About page lists the plain-text forms.
- DOC owns the final text; DATA supplies the dataset names, category, commit hash and sample size; NLTK and SPACY supply the exact library and model versions.
- Do not claim endorsement by Amazon, Yelp, NLTK, spaCy or the VADER authors.
