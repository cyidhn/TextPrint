#
# (Analyse) N-grammes
# Module Manager - TextPrint
#

# Importation des librairies
# spaCy
import spacy
from spacy import displacy
from pathlib import Path
import os
import re
import collections
import calendar
import time


# Traitement de lemmatisation
def traitement_lemmatisation(chemin):

    # Texte que l'on va analyser
    content = open(chemin, "r", encoding='utf8', errors="ignore")
    texte = content.read()
    texte = re.sub(r'[!"’«»#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '', texte)
    texte = texte.lower()
    content.close()

    # Impression
    ts = calendar.timegm(time.gmtime())
    impressionDoc = os.path.split(os.path.abspath(chemin))
    newDoc = impressionDoc[1].split(".")
    lienFinal = newDoc[0] + "_lem_" + str(ts) + ".html"
    newDoc = impressionDoc[0] + "/" + newDoc[0] + \
        "_lem_" + str(ts) + ".html"

    # Texte
    nlp = spacy.load('fr')
    tok = nlp(texte)
    tok = [token.lemma_ for token in tok]

    baseHtml = "<p>"
    for t in tok:
        baseHtml += t + " "
    baseHtml += "</p>"

    # Enregistrement des résultats
    output_path = Path(newDoc)
    linkDoc = "file://" + str(output_path)
    output_path.open("w", encoding="utf-8",
                     errors="ignore").write("<meta charset='utf-8'>" + baseHtml)

    return lienFinal
