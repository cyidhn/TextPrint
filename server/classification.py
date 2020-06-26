#
# Classification
# By Trang LAM & Jérémy DEMANGE
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
nltk.download('punkt')
nltk.download('stopwords')
