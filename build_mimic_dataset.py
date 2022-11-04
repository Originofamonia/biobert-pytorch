"""
from common labels with CTCXR, build mimic csv: labels + report
"""
import pandas as pd
import numpy as np
from glob import glob
import os
import re


def main():
    filepath = f"datasets/mimic_files"
    paths = []
    for root, dirs, files in os.walk(filepath):
        for file in files:
            paths.append(os.path.join(root, file))
    label_file = f'datasets/mimic-cxr-2.0.0-chexpert.csv'
    df = pd.read_csv(label_file)
    reports = []
    for file in paths:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines if x.strip()]  # remove "\n"
            start_index = [lines.index(l) for l in lines if l.startswith('INDICATION') or l.startswith('FINDINGS')]
            if len(start_index) > 0:
                label = 
                report = ' '.join(lines[start_index[0]:])
                reports.append(report)
            

if __name__ == '__main__':
    main()
