from nltk.corpus import wordnet as wn
import csv
import random

antonyms = {}
for synset in wn.all_synsets():
    #if synset.pos() in ['s', 'a']: # If synset is adj or satelite-adj.
    for lemma in synset.lemmas():
        if lemma.antonyms():
            for antonym in lemma.antonyms():
                pair = (lemma.name(), antonym.name())
                reversed_pair = (antonym.name(), lemma.name())
                if not reversed_pair in antonyms:
                    antonyms[pair] = [lemma.name(), antonym.name(), synset.pos(), lemma.key(), antonym.key(),
                                      synset.definition(), antonym.synset().definition()]



outfilename = "./antonyms.csv"
with open(outfilename, "w") as outfile:
    csvreader = csv.writer(outfile, delimiter="\t")
    header = ["pos_element", "neg_element", "POS", "pos_key", "neg_key", "pos_definition", "neg_definition"]
    csvreader.writerow(header)
    for pair in antonyms:
        row = antonyms[pair]
        csvreader.writerow(row)
