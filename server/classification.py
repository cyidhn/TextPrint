#
# Classification
# By Trang LAM
#


# Importations
import re
import time
import csv
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import json
import spacy
import torch
import string
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk import RegexpTokenizer
from nltk import word_tokenize
import os
import sys
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing.text import Tokenizer
# Tokenizer: a sentence with a list of string (tokens), split of string
from keras.preprocessing.sequence import pad_sequences
# Pad_sequences = all sequences have to have the same length
from keras.utils.np_utils import to_categorical
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model, model_to_dot
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model, Sequential, load_model
from keras import regularizers
from keras.initializers import Constant
from keras import optimizers
from IPython.display import SVG
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.callbacks import ModelCheckpoint
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

############################------#######################
# AF Import stopword list (Préciser la liste utilisé)


def load_stopwords(file_stopwords):
    lst_stopwords = []
    with open(file_stopwords, "r", encoding="utf-8") as file:
        for line in file:
            lst_stopwords.append(line.strip('\n'))
    return lst_stopwords


# AF Pour regex dans tokenizer
pattern_fr = "[a-zA-ZàâäèéêëîïôœùûüÿçÀÂÄÈÉÊËÎÏÔŒÙÛÜŸÇ-]"

# Create after a class or a def clean according to data type : mail or tweets or etc...


def clean_tweet(texte):
    # AF more comprehensive list, à tester et à adapter
    texte = re.sub(r'&gt;|&amp;|"', '', texte)
    # Erreurs en collectant les données: "c?est","d?un" => Remplacer "?"  par "'" - AF corrige les erreurs d'encodage
    texte = re.sub(r'(\w+?)\?(\w+?)', r"\1'\2", texte)
    #text=re.sub(r"(%s+')"%(pattern_fr),r'\1 ',text)
    # Remove RT@mention - AF Spécial pour les tweets Remove all retweet mentions. Optional.
    #text=re.sub(r'(RT|rt)[ ]*@[ ]*[\S]+',r'',text)
    # Remove mention ?? useful or not??  - AF justifier l'utilité d'un point de vu linguistique
    # text=re.sub(r'@[\S]+',r'',text)
    # Remove punctuations
    texte = re.sub(r'[!"’«»$%&()*+,./:;<=>?[\]^_`{|}~]', ' ', texte)
    return texte


def clean_mail(text):
    # Escape HTML characters
    text = re.sub('<.*?>', '', text)
    text = re.sub('/pre|e{0,2}&amp;lt;|e{0,2}&amp;gt;', ' ', text)
    text = re.sub('br ', '', text)
    # Remove digits: time (13h20,etc.)
    text = re.sub("\d+h\d{0,}|\d+", "", text)
    # Remove web adresses: http:// or https://, www.blabla.com,
    text = re.sub(r'\w+://\S+', '', text)
    text = re.sub(r'www.\S+', '', text)
    # Remove path for example: /home/httpd/htdocs/cumuli/poser_question2.php3
    text = re.sub(r'(/\w+){3,}/\S+', '', text)
    # Remove punctuations
    text = re.sub(r'[!"’«»#$%&()*+,./:;<=>?@[\]^_`{|}~]', ' ', text)
    # Remove (') in 'Interculture_prep'
    text = re.sub("\s'(.+?)'", r' \1 ', text)
    # Remove other unnecessary elements: punctuations ------------
    text = re.sub(r'[eE]\d[aA]\d', '', text)
    text = re.sub(r'-{2,}|- ', '', text)
    return text

# AF : n_words : Decide whether size of phrase is important, if yes select number of words. If 'None, don't apply. If number, then n = number.
# AF : use_stopwords if talse leave stopwords in text. If true, removes stopwords from text.


def tokenize(texte, n_words: int = None, use_stopwords=False):
    """
    Input: 
    texte
    n_words : in case of interesting in texte containing more than n_words 
    """
    # justifier pourquoi le choix de 4 mots
    # tokenizer=TweetTokenizer()
    tokenizer = RegexpTokenizer(r"%s+'|%s+|\S+" % (pattern_fr, pattern_fr))
    tokens = [tok.lower() for tok in tokenizer.tokenize(texte)]
    # Not working: review after. Currently replaced by if statement below.
    #tokens= [tok.lower() for tok in word_tokenize(text) if tok not in lst_stopwords] if use_stopwords else [tok.lower() for tok in word_tokenize(text)]
    if use_stopwords:
        lst_stopwords = load_stopwords("./models/stopwords.txt")
    else:
        lst_stopwords = []
    if n_words is not None:
        if len(tokens) >= n_words:
            tokens = [tok for tok in tokens if tok not in lst_stopwords]
            texte = " ".join(tokens)
        else:
            texte = np.nan
    else:
        tokens = [tok for tok in tokens if tok not in lst_stopwords]
        texte = " ".join(tokens)
    return texte


""""
def lemmatize(text):
  french_lemmatizer = LefffLemmatizer()
  #nlp.add_pipe(french_lemmatizer, name='lefff')
  tokens = [tok.lemma_ for tok in nlp(text)]
  return " ".join(tokens)
"""
# AF : implementé car le nombre max de tokens etablie est de 500 tokens. Limite établie par MAX SEQUENCE LENGTH, dans la fonction Prepare Data below.


def split_sent(textes, auteurs, max_sq_len):
    """
    To improve speed we will use a MAX_SEQUENCE_LENGTH shorter than the max lengthed sentence. 
    To avoid truncating sequences during padding we split our sentences to MAX_SEQUENCE_LENGTH and so the number of samples increases accordingly. 
    For example, if MAX_SEQUENCE_LENGTH=70, a sentence with length 150 splits in 3 sentences: 150=70+70+10
    """
    new_textes, new_auteurs = [], []
    for texte, auteur in zip(textes, auteurs):
        texte_tokens = [tok for tok in texte.split()]
        if len(texte_tokens) > max_sq_len:
            texte_split = [texte_tokens[x:x+max_sq_len]
                           for x in range(0, len(texte_tokens), max_sq_len)]
            auteur = [auteur]*len(texte_split)
            new_textes.extend([" ".join(sub_texte)
                               for sub_texte in texte_split])
            new_auteurs.extend(auteur)
        else:
            new_textes.extend([texte])
            new_auteurs.extend([auteur])
    return new_textes, new_auteurs

##################-----------######################


def longestSentence(textes):
    lst_tokens = []
    for texte in textes:
        lst_tokens.append([tok for tok in texte.split()])
    max_sq_len, longest_sent = max(
        [(len(tokens), tokens) for tokens in lst_tokens])
    return max_sq_len, longest_sent


###########################----------------------------#####################
def prepare_data(file_name, n_words=None, use_stopwords=False):
    """
    Input: file_csv, n_words (by default is None), using or not using stopwords (by default: not using Stopwords)
    The csv file must have a column containing texts and a column containing authors (the number of columns in file doesn't matter)
    """
    df = pd.read_csv(file_name, delimiter="\t", encoding="utf-8")
    while True:
        try:
            print(f"Your file has columns: {', '.join(df.columns)} ")
            auteurs = "auteur"
            textes = "tweet"
        except:
            pass
        # If the name of the column doesn't exist, print this error message
        if auteurs not in df.columns or textes not in df.columns:
            print(
                f"Please try again! The column's name doesn't exist.\nYour valid columns names are:{', '.join(df.columns)}")
        # If no errors, escape the loop
        else:
            break
    # Filter: keep only the authors who have more than 200 texts in dataset. Because if the number of text is too small => the model won't be trained properply => difficult to extract the features => problem for prediction
    df = df[df[auteurs].map(df[auteurs].value_counts()) > 200]
    if use_stopwords:
        if n_words is not None:
            df[textes] = df[textes].apply(lambda x: str(x)).apply(
                clean_tweet).apply(tokenize, n_words=n_words, use_stopwords=True)
        else:
            df[textes] = df[textes].apply(lambda x: str(x)).apply(
                clean_tweet).apply(tokenize, use_stopwords=True)
    else:
        if n_words is not None:
            df[textes] = df[textes].apply(lambda x: str(x)).apply(
                clean_tweet).apply(tokenize, n_words=n_words, use_stopwords=False)
        else:
            df[textes] = df[textes].apply(lambda x: str(x)).apply(
                clean_tweet).apply(tokenize, use_stopwords=False)
    df = df.dropna()
    # Transfomer les colonnes en des listes:
    # On obtient donc ici 2 listes: une liste d'auteurs + une liste de textes
    textes = df[textes].values.tolist()
    auteurs = df[auteurs].values.tolist()
    # Print the lenght + text of the longest text
    max_sq_len, longest_sent = longestSentence(textes)
    print(longest_sent)
    print("Max length: ", max_sq_len)
    # If the length of the longest text > 500, split that text into subtexts and each subset contains only 200 tokens.
    # For example: a text of length 700 will be split into 3 subtexts of length 200  and 1 subtext of lenght 100
    if max_sq_len > 500:
        print("Because the max_sequence_length is > 500. Max_sq_len will be set to 200")
        textes, auteurs = split_sent(textes, auteurs, 200)
    # Convert authors into the unique ID
    # For ex: authors =["author1","author2","author3","author2","author3",...]. After conversion, authors_encoded = [0,1,2,1,2,...]
    auteurs_encoded = np.array(auteurs)
    label_encoder = LabelEncoder()
    auteurs_encoded = label_encoder.fit_transform(auteurs_encoded)
    return textes, auteurs, auteurs_encoded


def split_data(textes, auteurs):
    """
    Split data into training set, test set and validation set:
    60% data for training, 20% for validation and 20% for testing
    """
    X_train, X_test, Y_train, Y_test = train_test_split(
        textes, auteurs, test_size=0.2)
    X_train, X_val, Y_train, Y_val = train_test_split(
        X_train, Y_train, test_size=0.25)
    return X_train, X_test, X_val, Y_train, Y_test, Y_val


def convert_data(textes, X_train, X_test, X_val, num_words: int = None):
    """
    Transfomer les textes en des fomats adaptés
    Tokenizer: = the tokenizer built by Keras, a simple tokenizer using blank space to tokenize 
    num_words: By default is None. Can define for example: 10000 to keep only 10000 most frequent words.
    filters: define the punctuations need to be removed 
    The default is all punctuation, plus tabs and line breaks, minus the ' character.
    For our case, minus also - character.
    """
    t = Tokenizer(num_words=num_words,
                  filters='!"$%&()*+,./:;<=>?[\\]^_`{|}~\t\n')
    t.fit_on_texts(textes)
    # convert to sequence of integers
    # Transforms each text in texts to a sequence of integers.
    # It takes each word in the text and replaces it with its corresponding integer value from the word_index dictionary.
    x_train = t.texts_to_sequences(X_train)
    x_val = t.texts_to_sequences(X_val)
    x_test = t.texts_to_sequences(X_test)
    # Word index: a dictionnary word-index based on word frequency
    word_index = t.word_index
    # The number of words
    if num_words is None:
        # Adding 1 because of reserved 0 index
        vocab_size = len(t.word_index) + 1
    else:
        vocab_size = num_words
    maxLen = len(max(x_train+x_val+x_test, key=len))  # longest text in data
    #maxLen1=max(len(x) for x in x_train+x_val+x_test)
    # Add pading to ensure all vectors have same dimensionality
    # Input of the model are vectors having same dimensionality
    x_train = pad_sequences(x_train, padding='post', maxlen=maxLen)
    x_val = pad_sequences(x_val, padding='post', maxlen=maxLen)
    x_test = pad_sequences(x_test, padding='post', maxlen=maxLen)
    return word_index, vocab_size, maxLen, x_train, x_val, x_test


def convert_labels(authors, Y_train, Y_val, Y_test):
    """
    Des labels vont se transformer en des one-hot vecteurs
    Example: if label is = 1 
    After being converted label = [0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
    """
    y_train = to_categorical(Y_train, num_classes=len(set(authors)))
    y_val = to_categorical(Y_val, num_classes=len(set(authors)))
    y_test = to_categorical(Y_test, num_classes=len(set(authors)))
    return y_train, y_val, y_test


# Gestion des tweets
# N_words=4: interesting only texts containing more than 4 words
textes, auteurs, auteurs_encoded = prepare_data(
    "./models/presidentielle.csv", n_words=5, use_stopwords=False)
X_train, X_test, X_val, Y_train, Y_test, Y_val = split_data(
    textes, auteurs_encoded)
# Use all vocab_size
# word_index,vocab_size,maxLen,x_train,x_val,x_test=convert_data(textes,X_train,X_test,X_val)
# Use only 30000 most frequent words
word_index, vocab_size, maxLen, x_train, x_val, x_test = convert_data(
    textes, X_train, X_test, X_val)
y_train, y_val, y_test = convert_labels(auteurs, Y_train, Y_val, Y_test)
dict_auteurs = dict(zip(auteurs_encoded, auteurs))

# Create a function to convert new data
tokenizer = Tokenizer(filters='!"$%&()*+,./:;<=>?[\\]^_`{|}~\t\n')
tokenizer.fit_on_texts(textes)


def convert_data_bis(tokenizer, sentences: list(), maxLen: int = 25):
    # convert to sequence of integers
    data = tokenizer.texts_to_sequences(sentences)
    data = pad_sequences(data, padding='post', maxlen=maxLen)
    return data


def result_classification(chemin="./static/textes/00test.txt", model="./models/model_twitter.h5"):

    # Convertir chemin en texte
    content = open(chemin, "r", encoding='utf8', errors="ignore")
    textes = content.read()
    content.close()

    # Ajout algo
    test = []
    test.append(textes)
    test_cleaned = list(map(clean_tweet, test))
    data = convert_data_bis(tokenizer, test_cleaned)

    # Load all model
    model2 = load_model(model)
    predict = model2.predict(data)
    print(predict)

    # probabilites
    for sentence, predict_auteur in zip(test, np.argmax(predict, axis=1).tolist()):
        auteur = dict_auteurs.get(predict_auteur)
        print(sentence)
        print("Auteur prédit pour le texte : ", auteur)
        return str(auteur)


result_classification()
