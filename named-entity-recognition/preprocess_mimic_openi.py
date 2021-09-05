
import pandas as pd
import csv


def filter_labels():
    mimic_filename = 'mimic-cxr-2.0.0-negbio.csv'
    openi_filename = 'indiana_reports.csv'
    mimic_df = pd.read_csv(mimic_filename)
    mimic_labels = mimic_df.columns.values[2:].tolist()
    mimic_labels = [mimic_disease.lower() for mimic_disease in mimic_labels]
    mimic_labels.append('normal')
    mimic_labels.remove('no finding')
    print(mimic_labels)

    openi_df = pd.read_csv(openi_filename)
    openi_mesh = openi_df.MeSH.values.tolist()
    openi_labels = []
    for mesh in openi_mesh:
        items = mesh.split(';')
        for item in items:
            if any(mimic_disease in item.lower() for mimic_disease in mimic_labels):
                openi_labels.append(item.split('/')[0])

    openi_labels = set(openi_labels)
    openi_labels = [openi_disease.lower() for openi_disease in openi_labels]
    print(openi_labels)

    common_labels = ['cardiomegaly', 'edema', 'opacity', 'pneumothorax',
                     'normal', 'consolidation', 'pneumonia', 'fracture',
                     'pleural effusion', 'atelectasis']

def make_mimic_df():
    mimic_filename = 'mimic-cxr-2.0.0-negbio.csv'
    common_labels = ['cardiomegaly', 'edema', 'opacity', 'pneumothorax',
                     'normal', 'consolidation', 'pneumonia', 'fracture',
                     'pleural effusion', 'atelectasis']


if __name__ == '__main__':
    # filter_labels()
    make_mimic_df()
