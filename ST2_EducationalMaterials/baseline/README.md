# Baseline System

The baseline system is based on [edit trees](https://doras.dcu.ie/550/1/GrzegorzPhDFinal.pdf) ([inspiration](https://aclanthology.org/P16-2090.pdf)).

The baseline works as follows.

Training:
- For each training example, it computes the edit tree between the source and the target sentence. (The edit tree represents modifications made to the source sentence to "reach" the target sentence.)
- For each indicated "Change" (i.e., column 3 in the data), edit trees associated with it are stored together with their frequency.

Testing:
- For "testing",  it attempts to modify a given source sentence according to a change to be conducted by appling all trees for that change in order of their frequency in the training data. It stops when an applicable tree is found, and outputs the result. If no applicable tree exists for a given source sentence and change, it outputs the source sentence.

## Installation

```
pip install -U spacy sacrebleu
```

## Running

```
python baseline_edit_trees.py ../data/bribri-train.tsv ../data/bribri-dev.tsv bribri-dev-prediction.tsv
```

## Evaluation

```
python evaluate.py bribri-dev-prediction.tsv
```

## Results

The main metric of the shared task is accuracy. BLEU and ChrF are provided as secondary metrics.

| Language | Accuracy |  BLEU | ChrF |
-----------|----------|-------|-------
Bribri     |     5.66 | 20.35 | 45.56
Guarani    |    22.78 | 34.99 | 77.14
Maya       |    26.17 | 52.38 | 78.72
Nahuatl    |     0.00 |  1.38 | 34.32

## No-op baseline

The no-op baseline just copies source sentence without any changes.
The code is provided in `baseline_noop.py`.

Results for the no-op baseline:

| Language | Accuracy |  BLEU | ChrF |
-----------|----------|-------|-------
Bribri     |     0.00 | 10.59 | 38.42
Guarani    |     0.00 | 23.33 | 71.47
Maya       |     0.00 | 33.67 | 69.15
Nahuatl    |     0.00 |  1.38 | 34.27
