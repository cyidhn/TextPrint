#
# (Analyse) Fiche des premieres statistiques
# Module Manager - TextPrint
#

# Importation des librairies
# spaCy
import spacy
from spacy import displacy

# WebView
# import webview
from pathlib import Path

# Detection de langue
from langdetect import detect

# Autre
import os
# from alerts import message_importation_reussie, message_langue_inconnue

# Thread
from threading import Thread
import re

# Fonction analyse global


def analyse_global(chemin, id_texte, n_version):

    # Texte que l'on va analyser
    content = open(chemin, "r", encoding='utf8', errors="ignore")
    texte = content.read()
    texte = re.sub(r'[!"’«»#$%&()*+,-./:;<=>?@[\]^_`{|}~]', '', texte)
    content.close()

    # Impression
    impressionDoc = os.path.split(os.path.abspath(chemin))
    newDoc = impressionDoc[1].split(".")
    newDoc = impressionDoc[0] + "/" + newDoc[0] + "_analyse.html"
    # print(newDoc)

    # Determiner la langue du document
    langue = detect(texte)

    # Choix de l'analyse de la langue
    nlp = spacy.load('fr')
    if (langue == 'fr'):
        nlp = spacy.load('fr')
    elif (langue == 'es'):
        nlp = spacy.load('es')
    elif (langue == 'en'):
        nlp = spacy.load('en')
    else:
        nlp = spacy.load('fr')
        print(
            "ERREUR - La langue du texte doit être en français, en anglais ou en espagnol.")
        # message_langue_inconnue()

    # Texte
    doc = nlp(texte)
    doc.user_data["title"] = "Analyse du texte"

    # Analyse du texte
    # Declaration des variables à analyser
    nbChars = len(texte)
    nbMots = len([token.text for token in doc if token.is_punct != True])
    nbPhrases = len(re.split(r'[.!?]+', texte))
    if nbPhrases == 0:
        nbPhrases = 1
    nbParagraphes = len(texte.split("\n"))

    nbNomsCommuns = len([token.text for token in doc if token.pos_ == 'NOUN'])
    nbVerbes = len([token.text for token in doc if token.pos_ == 'VERB'])
    nbAdjectifs = len([token.text for token in doc if token.pos_ == 'ADJ'])
    nbAdverbes = len([token.text for token in doc if token.pos_ == 'ADV'])

    nbArticlesDefinis = len([token.text for token in doc if (
        token.pos_ == 'DET' and (token.tag_).find('Definite=Def') != -1)])
    nbArticlesIndefinis = len([token.text for token in doc if (
        token.pos_ == 'DET' and (token.tag_).find('Definite=Ind') != -1)])
    nbPronomsPersonnels = len([token.text for token in doc if (
        token.pos_ == 'PRON' and (token.tag_).find('Person') != -1)])
    nbPronomsPossessifs = len([token.text for token in doc if (
        token.pos_ == 'PRON' and (token.tag_).find('Poss=Yes') != -1)])
    nbPronomsDemonstratifs = len([token.text for token in doc if (
        token.pos_ == 'PRON' and (token.tag_).find('PronType=Dem') != -1)])
    nbPronomsRelatifs = len([token.text for token in doc if (
        token.pos_ == 'PRON' and (token.tag_).find('PronType=Rel') != -1)])
    nbPronomsInterrogatifs = len([token.text for token in doc if (
        token.pos_ == 'PRON' and (token.tag_).find('PronType=Int') != -1)])
    nbPronomsIndefinis = len([token.text for token in doc if (
        token.pos_ == 'PRON' and (token.tag_).find('Dem') != -1)])
    nbPrepositions = len([token.text for token in doc if token.pos_ == 'ADP'])
    nbConjonctions = len([token.text for token in doc if token.pos_ == 'CONJ'])

    nbNombres = len([token.text for token in doc if token.pos_ == 'NUM'])

    # Sortie du texte
    """
    f = open(newDoc, "w")
    f.write('______')
    f.write('\nAnalyse du texte ')
    f.write('\n______ Langue ')
    f.write('\n_ Langue du texte : ')
    f.write(str(langue))
    f.write('\n______ Taille')
    f.write('\n_ Nombre de caractères : ')
    f.write(str(nbChars))
    f.write('\n_ Nombre de mots : ')
    f.write(str(nbMots))
    f.write('\n_ Nombre de phrases : ')
    f.write(str(nbPhrases))
    f.write('\n_ Nombre de paragraphes : ')
    f.write(str(nbParagraphes))
    f.write('\n______ Mots lexicaux')
    f.write('\n_ Noms communs : ')
    f.write(str(nbNomsCommuns))
    f.write('\n_ Verbes : ')
    f.write(str(nbVerbes))
    f.write('\n_ Adjectifs : ')
    f.write(str(nbAdjectifs))
    f.write('\n_ Adverbes : ')
    f.write(str(nbAdverbes))
    f.write('\n______ Mots grammaticaux')
    f.write('\n_ Articles définis : ')
    f.write(str(nbArticlesDefinis))
    f.write('\n_ Articles indéfinis : ')
    f.write(str(nbArticlesIndefinis))
    f.write('\n_ Pronoms personnels : ')
    f.write(str(nbPronomsPersonnels))
    f.write('\n_ Pronoms possessifs : ')
    f.write(str(nbPronomsPossessifs))
    f.write('\n_ Pronoms démonstratifs : ')
    f.write(str(nbPronomsDemonstratifs))
    f.write('\n_ Pronoms interrogatifs : ')
    f.write(str(nbPronomsInterrogatifs))
    f.write('\n_ Pronoms relatifs : ')
    f.write(str(nbPronomsRelatifs))
    f.write('\n_ Pronoms indéfinis : ')
    f.write(str(nbPronomsIndefinis))
    f.write('\n_ Prépositions : ')
    f.write(str(nbPrepositions))
    f.write('\n_ Conjonctions : ')
    f.write(str(nbConjonctions))
    f.write('\n______ Autres')
    f.write('\n_ Chiffres : ')
    f.write(str(nbNombres))
    f.close()
    """

    statsHtml = f"""
    <!--<b>Langue</b>-->
    <!--<p>Langue du texte : {str(langue)}</p>-->
    <b>Taille</b>
    <p>Nombre de caractères : {str(nbChars)}</p>
    <p>Nombre de mots : {str(nbMots)}</p>
    <p>Nombre de phrases : {str(nbPhrases)}</p>
    <p>Nombre de paragraphes : {str(nbParagraphes)}</p>
    <b>Mots lexicaux</b>
    <p>Noms communs : {str(nbNomsCommuns)}</p>
    <p>Verbes : {str(nbVerbes)}</p>
    <p>Adjectifs : {str(nbAdjectifs)}</p>
    <p>Adverbes : {str(nbAdverbes)}</p>
    <b>Mots grammaticaux</b>
    <p>Articles définis : {str(nbArticlesDefinis)}</p>
    <p>Articles indéfinis : {str(nbArticlesIndefinis)}</p>
    <p>Pronoms personnels : {str(nbPronomsPersonnels)}</p>
    <p>Pronoms possessifs : {str(nbPronomsPossessifs)}</p>
    <p>Pronoms démonstratifs : {str(nbPronomsDemonstratifs)}</p>
    <p>Pronoms interrogatifs : {str(nbPronomsInterrogatifs)}</p>
    <p>Pronoms relatifs : {str(nbPronomsRelatifs)}</p>
    <p>Pronoms indéfinis : {str(nbPronomsIndefinis)}</p>
    <p>Prépositions : {str(nbPrepositions)}</p>
    <p>Conjonctions : {str(nbConjonctions)}</p>
    <b>Autres</b>
    <p>Chiffres : {str(nbNombres)}</p>
    """

    # Fichier html
    baseHtml = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Analyse du texte</title>
            <meta charset="utf-8">
        </head>
        <body>
            <div class="container mt-3">
                <h1 class="text-center font-weight-bold">Texte 1</h1>
                <h3 class="text-center">Version : 1</h3>
                <hr>
                <h5>// Fiche de statistiques :</h5>
                %(stats)s
                <hr>
            </div>
        </body>
    </html>
    """ % {"stats": statsHtml}

    # Message importation reussie
    # message_importation_reussie()

    # Enregistrer et afficher en WebView
    output_path = Path(newDoc)
    linkDoc = "file://" + str(output_path)
    print(linkDoc)
    output_path.open("w", encoding="utf-8",
                     errors="ignore").write("<meta charset='utf-8'>" + baseHtml)

    # Afficher le texte du fichier
    # init_window(f)
    #fichier = open(newDoc, "r")
    #label = Label(f, text="ANALYSE DE TEXTES")
    #label.pack(side=TOP, padx=10, pady=30)
    # fichier.close()

    # On lance un Thread pour continuer a voir la fenetre
    # webview.create_window('Analyse de texte', linkDoc)
    # webview.start()
