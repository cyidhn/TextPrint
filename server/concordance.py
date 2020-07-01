import nltk.corpus
from nltk.tokenize import WordPunctTokenizer
from nltk.text import Text

t = nltk.tokenize.WordPunctTokenizer()
c = Text(t.tokenize(
    "Bonjour ceci est un test avec un faux texte. Ceci est un deuxième test également."))
c.concordance(u'test')
