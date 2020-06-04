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


# Fonction pour générer soi-même son propre nombre de n-grams de mots
def ngrams(tokens, n):
    # On retourne un tableau avec le nombre de n choisis
    return zip(*[tokens[i:] for i in range(n)])


# Fonction pour générer soi-même son propre nombre de n-grams de chars
def ngramsChars(tokens, n, exact=True):
    # Pretraitement
    text = ""
    for t in tokens:
        text += t
    # On retourne un tableau avec le nombre de n choisis
    return ["".join(j) for j in zip(*[text[i:] for i in range(n)])]


# Création de la fonction pour compter les n-grams
def model_n_exists(ngrams, number):
    counter = collections.Counter()
    for n in ngrams:
        count = []
        myWords = ""
        for mots in n:
            myWords += mots + " "
        count.append(myWords)
        # counter.update(set(zip(n[:-1], n[1:])))
        counter.update(set(count))
    return counter


# Fonction N-grammes
def analyse_ngrammes_mots(chemin, n_grammes, n_version=2):

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
    lienFinal = newDoc[0] + "_ngrammes_" + str(ts) + ".html"
    newDoc = impressionDoc[0] + "/" + newDoc[0] + \
        "_ngrammes_" + str(ts) + ".html"

    # Texte
    nlp = spacy.load('fr')
    tok = nlp(texte)
    tok = [token.text for token in tok if token.is_alpha]

    # Résultats
    N2result = list(ngrams(tok, n_grammes))
    resultat = model_n_exists(N2result, n_grammes)

    # Boucle résultat
    baseHtml = ""
    for r in resultat.most_common():
        baseHtml += "<b>" + str(r[0]) + "</b><br/>"
        baseHtml += "Nombre de segments répétés : " + str(r[1]) + "<br/><br/>"

    # Enregistrement des résultats
    output_path = Path(newDoc)
    linkDoc = "file://" + str(output_path)
    output_path.open("w", encoding="utf-8",
                     errors="ignore").write("<meta charset='utf-8'>" + baseHtml)

    return lienFinal


# Fonction N-grammes
def analyse_ngrammes_chars(chemin, n_grammes=2, n_version=3):

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
    lienFinal = newDoc[0] + "_ngrammes_chars_" + str(ts) + ".html"
    newDoc = impressionDoc[0] + "/" + newDoc[0] + \
        "_ngrammes_chars_" + str(ts) + ".html"

    # Texte
    nlp = spacy.load('fr')
    tok = nlp(texte)
    tok = [token.text for token in tok if token.is_alpha]

    # Résultats
    N2result = list(ngramsChars(tok, n_grammes))
    resultat = model_n_exists(N2result, n_grammes)

    # Boucle résultat
    baseHtml = ""
    for r in resultat.most_common():
        baseHtml += "<b>" + str(r[0]) + "</b><br/>"
        baseHtml += "Nombre de segments répétés : " + str(r[1]) + "<br/><br/>"

    # Enregistrement des résultats
    output_path = Path(newDoc)
    linkDoc = "file://" + str(output_path)
    output_path.open("w", encoding="utf-8",
                     errors="ignore").write("<meta charset='utf-8'>" + baseHtml)

    return lienFinal


# New
def analyse_ngrammes_pos(chemin, n_grammes, n_version=2):

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
    lienFinal = newDoc[0] + "_ngrammes_" + str(ts) + ".html"
    newDoc = impressionDoc[0] + "/" + newDoc[0] + \
        "_ngrammes_" + str(ts) + ".html"

    # Texte
    nlp = spacy.load('fr')
    tok = nlp(texte)
    tok = [token.tag_ for token in tok if token.is_alpha]

    # Résultats
    N2result = list(ngrams(tok, n_grammes))
    resultat = model_n_exists(N2result, n_grammes)

    # Boucle résultat
    baseHtml = ""
    for r in resultat.most_common():
        baseHtml += "<b>" + str(r[0]) + "</b><br/>"
        baseHtml += "Nombre de segments répétés : " + str(r[1]) + "<br/><br/>"

    # Enregistrement des résultats
    output_path = Path(newDoc)
    linkDoc = "file://" + str(output_path)
    output_path.open("w", encoding="utf-8",
                     errors="ignore").write("<meta charset='utf-8'>" + baseHtml)

    return lienFinal


# Test
# analyse_ngrammes_mots("./static/textes/1578865117.txt",
#                       n_grammes=4, n_version=2)
# print(analyse_ngrammes_chars(
#     "./static/textes/1578865117.txt", n_grammes=4, n_version=2))
