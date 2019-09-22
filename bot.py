import requests  
from bottle import (  
    run, post, response, request as bottle_request
)
BOT_URL = 'https://api.telegram.org/bot867872213:AAFBdCwZ77WtonOwQpCGX2suYWtsEzbvxU8/' # <--- add your telegram token here; it should be like https://api.telegram.org/bot12345678:SOMErAn2dom/

'''
TRUMP - TextBot
A simple NLTK Text Chatbot for the "Tag der Talente" workshop 2019 
based on an example script from Parul Pandey.
'''
import io
import os
import random
import string # (Zur Verarbeitung von Standard Python Strings)
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from stop_words import get_stop_words
from termcolor import colored, cprint
import nltk
from nltk.stem import WordNetLemmatizer

warnings.filterwarnings('ignore')

# Begrüßungen
GREETING_INPUTS = ("hello", "hi", "what`s up","what is up")
GREETING_RESPONSES = ["Make America Great Again!!!", "Part of my beauty is that I am very rich!"]
GREETING_INPUTS = ("hello", "hi")
GREETING_RESPONSES = ["hi", "hey", "what's up", "Good afternoon", "hello", "It's nice meet you", "Make America Great Again!!!", "Part of my beauty is that I am very rich!"]

# Beleidigungen
INDIGNITY_INPUTS = ("cunt", "robot", "bot", "nigga", "stupid", "asshole", "fuck")
INDIGNITY_RESPONSES = ["You're fired", "We gonna build a wall around you", "Fake News", "You are like Obama", "Mexicunt", "Stupid European", "Bitch"]

# Komplimente
COMPLIMENT_INPUTS = ("nice", "sexy", "clever", "humanoid", "talented", "trumpy")
COMPLIMENT_RESPONSES = ["thanks", "You too", "You're almost so amazing as Trump"]


#Jokes
JOKES_INPUT=['North Koreans believe they live in the best country in the world because they\'re brainwashed by the government and the media.\nWhen every American knows that America is the best country in the world.', 
'You enter the laboratory and see an experiment. How will you know which class is it?\nIf it\'s green and wiggles, it\'s biology.\nIf it stinks, it\'s chemistry.\nIf it doesn\'t work, it\'s physics.',
'What\'s the difference between Americans and yogurt\?\n If you leave yogurt alone for 300 years\, it\'ll grow a culture.']


# nltk.download('popular', quiet=True)

# # Für den ersten Start, ansonsten auskommentieren
# nltk.download('punkt')
# nltk.download('wordnet')


# Corpus einlesen
# with open('chatbot_de.txt','r', encoding='utf8', errors ='ignore') as bockwurst:
#     raw = bockwurst.read().lower()

with open("new.txt",'r', encoding='utf8', errors ='ignore') as tweet1file:
    raw = tweet1file.read().lower()

with open(os.path.join("json", "trump_data_file.txt"),'r', encoding='utf8', errors ='ignore') as tweet2file:
    raw = tweet2file.read().lower()

# Tokenisierung
# sent_tokens konvertiert in Liste von Sätzen
sent_tokens = nltk.sent_tokenize(raw)
# word_tokens konvertiert in Liste von Worten (Wird nicht verwendet.)
word_tokens = nltk.word_tokenize(raw)

# Vorverarbeitung (Preprocessing)
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
def trivia(sentence):
    '''Wenn die Nutzereingabe eine Begrüßung ist, Antwortet der Bot mit einer zufälligen Begrüßung als Antwort,
    gleiches gilt für Beleidigungen'''
    for word in sentence.split():
        if random.randint(1,10) <= 3:
            return random.choice(["42","Satz von Gong","Möge Frau Karl... zurücktreten"])
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
        if word.lower() in COMPLIMENT_INPUTS:
            return random.choice(COMPLIMENT_RESPONSES)
        if word.lower() in INDIGNITY_INPUTS:
            return random.choice(INDIGNITY_RESPONSES)

# Antwort Erzeugung
def response(user_response):
    stop_words = get_stop_words('german')
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=stop_words)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    robo_response="TFIDX["+str(round(req_tfidf,2))+"]"
    if(req_tfidf==0):
        robo_response=robo_response+ "Wie bitte? Meintest du \'Satz von Gong\'?"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

def get_chat_id(data):
    chat_id = data['message']['chat']['id']
    return chat_id

def get_message(data):
    message_text = data['message']['text']
    return message_text

def send_message(prepared_data):
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib

def change_text_message(text):
    return text[::-1]

def prepare_data_for_answer(data):  
    user_response = get_message(data).lower()
    answer = ""
    tmp = trivia(user_response)
    if(user_response=='danke dir' or user_response=='danke' ):
        answer = 'Gerne..'
    elif tmp!=None:
        answer = tmp
    else:
        answer = response(user_response)
    json_data = {
        "chat_id": get_chat_id(data),
        "text": answer,
    }
    return json_data

@post('/')
def main():  
    data = bottle_request.json
    answer_data = prepare_data_for_answer(data)
    send_message(answer_data)  # <--- function for sending answer
    return response  # status 200 OK by default

if __name__ == '__main__':  
    run(host='localhost', port=8080, debug=True)