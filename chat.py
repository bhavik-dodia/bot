from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import os
import json
import nltk
import pickle
import random
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

nltk.download('wordnet')
nltk.download('punkt')
lemmatizer = WordNetLemmatizer()

model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json', encoding='utf8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def chat(inp):
    res = model.predict(np.array([bow(inp, words,show_details=False)]))[0]
    res_index = np.argmax(res)
    tag = classes[res_index]
    if res[res_index] > 0.8:
        for tg in intents['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']
        return random.choice(responses)
    else:
        return random.choice(["Sorry, I didn't get that, try something else! 🧐🤔", "Sorry, I can't understand, try changing words! 🧐🤔"])