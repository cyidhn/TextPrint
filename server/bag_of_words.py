from keras.preprocessing.text import Tokenizer

sentence = ["Bonjour Jérémy, merci d'être là aujourd'hui pour parler d'intéreprétation avec le bag of words. C'est très agréable. Le bag of words est quelque chose de très important, à ne pas négliger !"]


def print_bow(sentence: str) -> None:
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sentence)
    sequences = tokenizer.texts_to_sequences(sentence)
    word_index = tokenizer.word_index
    bow = {}
    for key in word_index:
        bow[key] = sequences[0].count(word_index[key])
    print(f'Nous avons trouvé {len(word_index)} tokens uniques.')
    print(f"Bag of words du texte :")
    for b in bow:
        print(b, '->', str(bow[b]))


print_bow(sentence)
