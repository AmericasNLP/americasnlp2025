#!/usr/bin/env python3

import csv
import sys

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} train.tsv dev.tsv dev-prediction.tsv")
    sys.exit(1)

train_path = sys.argv[1]
dev_path = sys.argv[2]
dev_prediction_path = sys.argv[3]

with open(dev_path, newline="", encoding="utf-8") as ifile, open(
    dev_prediction_path, "w", newline="", encoding="utf-8"
) as ofile:
    icsv = csv.DictReader(ifile, delimiter="\t")
    fieldnames = icsv.fieldnames
    fieldnames.append("Predicted Target")

    ocsv = csv.DictWriter(ofile, fieldnames=fieldnames, delimiter="\t")
    ocsv.writeheader()

    for row in icsv:
        row["Predicted Target"] = row["Source"]
        ocsv.writerow(row)
