import csv
import pandas as pd
from sklearn.metrics import cohen_kappa_score

def get_annotations(filename):
    dict_annotations = {}
    with open(filename) as infile:
        csvfile = csv.DictReader(infile, delimiter="\t")
        rows = list(csvfile)
        for row in rows[1:]:
            pair = (row["pos_element"], row["neg_element"])
            dict_annotations[pair] = row
    #print(dict_annotations)
    return dict_annotations

def calculate_agreement_affixals(annotations_1, annotations_2):
    """
    Returns an agreement score (Cohen's kappa) for affixal/non-affixal
    """
    affixals_1 = []
    affixals_2 = []
    # Search for pairs annotated by both and append those to lists
    for pair in annotations_1:
        if pair in annotations_2:
            affixals_1.append(annotations_1[pair]["affixal"])
            affixals_2.append(annotations_2[pair]["affixal"])
    n = len(affixals_1)
    kappa = cohen_kappa_score(affixals_1, affixals_2)
    return n, kappa

def calculate_agreement_directness(annotations_1, annotations_2):
    """
    Returns an agreement score (Cohen's kappa) for direct/indirect
    """
    directness_1 = []
    directness_2 = []
    # Search for pairs annotated by both
    for pair in annotations_1:
        if pair in annotations_2:
            # Only take those into account that were annotated as "affixal" by both annotators and add those to lists
            if annotations_1[pair]["affixal"] == "affixal" and annotations_2[pair]["affixal"] == "affixal":
                directness_1.append(annotations_1[pair]["directness"])
                directness_2.append(annotations_2[pair]["directness"])
    n = len(directness_1)
    kappa = cohen_kappa_score(directness_1, directness_2)
    return n, kappa

def calculate_agreement_subtypes_all(annotations_1, annotations_2):
    """
    Returns an agreement score (Cohen's kappa) and a confusion matrix for the subtypes
    """
    subtypes_1 = []
    subtypes_2 = []
    # Search for pairs annotated by both
    for pair in annotations_1:
        if pair in annotations_2:
            # Only take those into account that were annotated as "affixal" by both annotators and add those to lists
            # (include NA as subtype)
            if all([annotations_1[pair]["affixal"] == "affixal",
                    annotations_2[pair]["affixal"] == "affixal"]):
                subtypes_1.append(annotations_1[pair]["subtype"])
                subtypes_2.append(annotations_2[pair]["subtype"])
    # Get number of instances
    n = len(subtypes_1)
    # Calculate Cohen's kappa
    kappa = cohen_kappa_score(subtypes_1, subtypes_2)
    # Create confusion matrix
    series_1 = pd.Series(subtypes_1, name='Subtypes_1')
    series_2 = pd.Series(subtypes_2, name='Subtypes_2')
    confusion_matrix = pd.crosstab(series_1, series_2)
    return n, kappa, confusion_matrix

def calculate_agreement_subtypes_indirect(annotations_1, annotations_2):
    """
    Returns an agreement score (Cohen's kappa) and a confusion matrix for the subtypes
    """
    subtypes_1 = []
    subtypes_2 = []
    # Search for pairs annotated by both
    for pair in annotations_1:
        if pair in annotations_2:
            # Only take those into account that were annotated as "affixal" and "indirect"
            # by both annotators and add those to lists
            if all([annotations_1[pair]["affixal"] == "affixal",
                    annotations_2[pair]["affixal"] == "affixal",
                    annotations_1[pair]["directness"] == "indirect",
                    annotations_2[pair]["directness"] == "indirect"]):
                subtypes_1.append(annotations_1[pair]["subtype"])
                subtypes_2.append(annotations_2[pair]["subtype"])
    # Get number of instances
    n = len(subtypes_1)
    # Calculate Cohen's kappa
    kappa = cohen_kappa_score(subtypes_1, subtypes_2)
    # Create confusion matrix
    series_1 = pd.Series(subtypes_1, name='Subtypes_1')
    series_2 = pd.Series(subtypes_2, name='Subtypes_2')
    confusion_matrix = pd.crosstab(series_1, series_2)
    return n, kappa, confusion_matrix


def show_disagreements(annotations_1, annotations_2, element):
    n = 1
    for pair in annotations_1:
        if pair in annotations_2:
            if annotations_1[pair][element] != annotations_2[pair][element]:
                print(pair, annotations_1[pair][element], annotations_2[pair][element])
                n += 1
    print(n)
    return

def show_disagreements_directness(annotations_1, annotations_2):
    n = 1
    for pair in annotations_1:
        if pair in annotations_2:
            if annotations_1[pair]["affixal"] == "affixal" and annotations_2[pair]["affixal"] == "affixal":
                if annotations_1[pair]["directness"] == annotations_2[pair]["directness"]:
                    print(pair, annotations_1[pair]["directness"], annotations_2[pair]["directness"],
                          annotations_1[pair]["subtype"], annotations_2[pair]["subtype"])
                    n += 1
    print(n)
    return

def show_disagreements_subtype(annotations_1, annotations_2):
    n = 1
    for pair in annotations_1:
        if pair in annotations_2:
            if all([annotations_1[pair]["affixal"] == "affixal",
                    annotations_2[pair]["affixal"] == "affixal",
                    annotations_1[pair]["directness"] == "indirect",
                    annotations_2[pair]["directness"] == "indirect"]):
                if annotations_1[pair]["subtype"] != annotations_2[pair]["subtype"]:
                    print(pair, annotations_1[pair]["subtype"], annotations_2[pair]["subtype"])
                    n += 1
    print(n)
    return

# read annotations
annotations_1 = get_annotations("../annotations/annotator1.txt")
annotations_2 = get_annotations("../annotations/annotator2.txt")

# calculate IAA for affixal/non-affixal
n_affixal, kappa_affixal = calculate_agreement_affixals(annotations_1, annotations_2)
print("Agreement on affixal/non-affixal (Cohen's kappa):", kappa_affixal, "(n = %s)" % n_affixal)

# calculate IAA for direct/indirect
n_directness, kappa_directness = calculate_agreement_directness(annotations_1, annotations_2)
print("Agreement on direct/indirect (Cohen's kappa):", kappa_directness, "(n = %s)" % n_directness)

# calculate IAA for subtypes + print confusion matrix
n_subtypes_indirect, kappa_subtypes_indirect, confusion_subtypes_indirect = calculate_agreement_subtypes_indirect(annotations_1, annotations_2)
n_subtypes_all, kappa_subtypes_all, confusion_subtypes_all = calculate_agreement_subtypes_all(annotations_1, annotations_2)

print("Agreement on subtypes - indirect (Cohen's kappa):", kappa_subtypes_indirect, "(n = %s)" % n_subtypes_indirect)
print("\nConfusion matrix for subtypes (indirect only):\n", confusion_subtypes_indirect, "\n\n")

print("Agreement on subtypes - all (Cohen's kappa):", kappa_subtypes_all, "(n = %s)" % n_subtypes_all)
print("\nConfusion matrix for subtypes (all - including NA=direct):\n", confusion_subtypes_all)

# Printing disagreements
print("\nDisagreements on affixal:")
show_disagreements(annotations_1, annotations_2, "affixal")
print("\nDisagreements on direct/indirect:")
show_disagreements_directness(annotations_1, annotations_2)
print("\nDisagreements on subtype:")
show_disagreements_subtype(annotations_1, annotations_2)
