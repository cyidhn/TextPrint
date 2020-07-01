from keras.preprocessing.text import Tokenizer
import calendar
import time
import os
import re
from pathlib import Path


# Traitement de lemmatisation
def traitement_bagofwords(chemin):

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
    lienFinal = newDoc[0] + "_bow_" + str(ts) + ".html"
    newDoc = impressionDoc[0] + "/" + newDoc[0] + \
        "_bow_" + str(ts) + ".html"

    sentence = []
    sentence.append(texte)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sentence)
    sequences = tokenizer.texts_to_sequences(sentence)
    word_index = tokenizer.word_index
    bow = {}
    for key in word_index:
        bow[key] = sequences[0].count(word_index[key])
    baseHtml = f"<p>Nous avons trouvé {len(word_index)} tokens uniques.</p><br>"
    baseHtml += f"<p>Bag of words du texte :</p>"
    for b in bow:
        baseHtml += f"<p><b>{str(b)}</b> -> {str(bow[b])}</p>"

    # Enregistrement des résultats
    output_path = Path(newDoc)
    linkDoc = "file://" + str(output_path)
    output_path.open("w", encoding="utf-8",
                     errors="ignore").write("<meta charset='utf-8'>" + baseHtml)

    return lienFinal
