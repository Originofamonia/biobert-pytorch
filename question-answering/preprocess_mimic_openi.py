import pandas as pd
import csv
import os
import math


def filter_labels():
    abs_current_path = os.path.realpath('./')
    print(abs_current_path)
    mimic_filename = 'datasets/mimic-cxr-2.0.0-negbio.csv'
    openi_filename = 'datasets/indiana_reports.csv'
    mimic_df = pd.read_csv(mimic_filename)
    mimic_labels = mimic_df.columns.values[2:].tolist()
    mimic_labels = [mimic_disease.lower() for mimic_disease in mimic_labels]
    # mimic_labels.append('normal')
    # mimic_labels.remove('no finding')
    print(mimic_labels)

    openi_df = pd.read_csv(openi_filename)
    openi_mesh = openi_df.MeSH.values.tolist()
    openi_labels = []
    for mesh in openi_mesh:
        items = mesh.split(';')
        for item in items:
            if any(mimic_disease in item.lower() for mimic_disease in
                   mimic_labels):
                openi_labels.append(item.split('/')[0])

    openi_labels = set(openi_labels)
    # openi_labels = [openi_disease.lower() for openi_disease in openi_labels]
    print(openi_labels)

    common_labels = ['cardiomegaly', 'edema', 'pneumothorax',
                     'normal', 'consolidation', 'pneumonia', 'fracture',
                     'pleural effusion', 'atelectasis']


def make_mimic_df():
    """
    filter original label to common labels and make a new csv, still no findings
    """
    mimic_filename = '../datasets/mimic-cxr-2.0.0-negbio.csv'
    common_labels = ['cardiomegaly', 'edema', 'pneumothorax',
                     'no finding', 'consolidation', 'pneumonia', 'fracture',
                     'pleural effusion', 'atelectasis']
    new_columns = ['subject_id', 'study_id', 'Atelectasis', 'Cardiomegaly',
                   'Consolidation', 'Edema', 'Fracture', 'No Finding',
                   'Pleural Effusion', 'Pneumonia', 'Pneumothorax']
    df = pd.read_csv(mimic_filename)
    df2 = pd.DataFrame(columns=new_columns)
    # 1. remove not common columns
    for disease in df.columns.values[2:]:
        if disease.lower() not in common_labels:
            df = df.drop(disease, axis=1)

    print(df.head())
    # 2. iterate all examples, select qualified example and put to new df
    for index, row in df.iterrows():
        row_dict = row[2:].to_dict()
        if 1.0 in row_dict.values():
            row_head = row[:2].to_dict()
            for key, value in row_head.items():
                row_head[key] = int(value)

            for key, value in row_dict.items():
                if value != 1.0:
                    row_dict[key] = 0
                else:
                    row_dict[key] = 1
            row_head.update(row_dict)
            df2 = df2.append(row_head, ignore_index=True)

    # 3. save new df2
    print(df2.head)
    df2.to_csv('filtered_mimic.csv', index=False)


def add_findings_to_mimic():
    df = pd.read_csv(
        '/home/qiyuan/2021fall/biobert-pytorch/question-answering/filtered_mimic.csv')
    for index, row in df.iterrows():
        subject_id = row['subject_id']
        study_id = row['study_id']
        report_path = f'/home/qiyuan/2021fall/biobert-pytorch/datasets/mimic_files/p{subject_id}/s{study_id}.txt'
        with open(report_path) as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if 'FINDINGS' in line:
                    start_index = i + 1
                if 'IMPRESSION' in line:
                    end_index = i
            findings = [line.strip('\n') for line in
                        lines[start_index: end_index]]
            finding = ''.join(findings).strip()
            df.loc[index, 'findings'] = finding

    df.to_csv('mimic_w_findings.csv', index=False)


def make_openi_df():
    openi_filename = '/home/qiyuan/2021fall/biobert-pytorch/datasets/indiana_reports.csv'
    common_labels = ['cardiomegaly', 'edema', 'pneumothorax',
                     'normal', 'consolidation', 'pneumonia', 'fracture',
                     'pleural effusion', 'atelectasis']
    new_columns = ['cardiomegaly', 'edema', 'pneumothorax',
                   'normal', 'consolidation', 'pneumonia', 'fracture',
                   'pleural effusion', 'atelectasis', 'findings']
    df = pd.read_csv(openi_filename)
    df2 = pd.DataFrame(columns=new_columns)
    for index, row in df.iterrows():
        mesh = row['MeSH']
        finding = row['findings']
        if not isinstance(finding, str):
            continue
        item_labels = []
        items = mesh.split(';')
        for item in items:
            if any(mimic_disease in item.lower() for mimic_disease in
                   common_labels):
                split_item = item.lower().split('/')[0]
                item_labels.append(split_item)
        row_dict = {'findings': finding}
        for label in common_labels:
            if label in item_labels:
                row_dict[label] = 1
            else:
                row_dict[label] = 0
        # if 1 not in row_dict.values():
        #     continue
        df2 = df2.append(row_dict, ignore_index=True)
    df2.to_csv('filtered_openi.csv', index=False)
    print(df2.head())


if __name__ == '__main__':
    # filter_labels()
    # make_mimic_df()
    # add_findings_to_mimic()
    make_openi_df()
