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
import math
import pyttsx3
engine = pyttsx3.init("dummy")
isPlayingPrimesGame = False
isPlayingWealthGame = False

warnings.filterwarnings('ignore')

# Begrüßungen
GREETING_INPUTS = ("hello", "hi", "good afternoon", "greetings", "servus")
GREETING_RESPONSES = ["Make America Great Again!!!", "Part of my beauty is that I am very rich!", "hi", "hey", "what's up", "Good afternoon", "hello", "It's nice to meet you", "Make America Great Again!!!", "Part of my beauty is that I am very rich!"]

# Beleidigungen
INDIGNITY_INPUTS = ("motherfucker", "bitch", "cunt", "robot", "bot", "nigga", "stupid", "asshole", "fuck")
INDIGNITY_RESPONSES = ["'You do know you just attacked a Gold Star family?","I’m speaking with myself, number one, because I have a very good brain and I’ve said a lot of things.","My fingers are long and beautiful, as, it has been well been documented, are various other parts of my body","Sorry losers and haters, but my I.Q. is one of the highest—and you all know it! Please don't feel so stupid or insecure. It's not your fault""You're fired", "We gonna build a wall around you", "Fake News", "You are like Obama", "Mexicunt", "Stupid European", "Bitch"]

# Komplimente
COMPLIMENT_INPUTS = ("nice", "sexy", "clever", "humanoid", "talented", "trumpy")
COMPLIMENT_RESPONSES = ["Let me tell you, I'm a really smart guy.","thanks", "You too", "You're almost as amazing as Trump", "I think I am, actually humble. I think I'm much more humble than you would understand","The beauty of me is that I'm very rich"]

# Reaktionen
REACTION_INPUTS = [GREETING_INPUTS, INDIGNITY_INPUTS, COMPLIMENT_INPUTS]
REACTION_RESPONSES = [GREETING_RESPONSES, INDIGNITY_RESPONSES, COMPLIMENT_RESPONSES]

# Help
HELP_INPUTS = "help"
HELP_RESPONSES = "I am very good at interacting with humans. You may ask for \"greetings\", \"swears\" or \"compliments\" to get further information about my socialskills."

# Help Begrüßungen
GREETINGHELP_INPUTS = "greetings"
GREETINGHELP_RESPONSES = "If you want me to greet you. First you will have to say something like \"Make America Great Again!!!\", \"Part of my beauty is that I am very rich!\", \"hi\", \"hey\", \"what's up\", \"Good afternoon\", \"hello\", \"It's nice to meet you\", \"Make America Great Again!!!\", \"Part of my beauty is that I am very rich!\""

# Help Beleidigungen
INDIGNITYHELP_INPUTS = "swears"
INDIGNITYHELP_RESPONSES = "If you swear at me, I will fire back. Don't even think about saying something like: \"motherfucker\", \"bitch\", \"cunt\", \"robot\", \"bot\", \"nigga\", \"stupid\", \"asshole\" or \"fuck\""

# Help Komplimente
COMPLIMENTHELP_INPUTS = "compliments"
COMPLIMENTHELP_RESPONSES = "I looove compliments. Please say something like \"nice\", \"sexy\", \"clever\", \"humanoid\", \"talented\" or \"trumpy\""

# Hilfsreaktionen
HELPREACTION_INPUTS = [HELP_INPUTS, GREETINGHELP_INPUTS, INDIGNITYHELP_INPUTS, COMPLIMENTHELP_INPUTS]
HELPREACTION_RESPONSES = [HELP_RESPONSES, GREETINGHELP_RESPONSES, INDIGNITYHELP_RESPONSES, COMPLIMENTHELP_RESPONSES]

# nltk.download('popular', quiet=True)
nltk.download('popular', quiet=True)

# # Für den ersten Start, ansonsten auskommentieren
nltk.download('punkt')
nltk.download('wordnet')


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
    '''Wenn die Nutzereingabe in Begrüßung ist, Antwortet der Bot mit einer zufälligen Begrüßung als Antwort,
    gleiches gilt für Beleidigungen'''
    for word in sentence.split():
        for reaction in range(len(REACTION_INPUTS)):
            if word.lower() in REACTION_INPUTS[reaction]:
                return random.choice(REACTION_RESPONSES[reaction])
        for Help in range(len(HELPREACTION_INPUTS)):
            if word.lower() in HELPREACTION_INPUTS[Help]:
                return HELPREACTION_RESPONSES[Help]

# Antwort Erzeugung
def response1(user_response):
    stop_words = get_stop_words('english')
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=stop_words,ngram_range=(1, 10))
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    i = random.randint(2,14)
    idx=vals.argsort()[0][-i]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-i]
    if req_tfidf == 0:
        idx = vals.argsort()[0][-2]
        req_tfidf = flat[-2]
    robo_response="TFIDX["+str(round(req_tfidf,2))+"]"
    if(req_tfidf==0):

        robo_response=robo_response+ "I beg your pardon, asshole? Did you mean \'Gong's theorem\'?"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

#Telegram Part
def get_chat_id(data):
    chat_id = data['message']['chat']['id']
    return chat_id

def get_message(data):
    message_text = data['message']['text']
    return message_text

def send_message(prepared_data):
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib

def prepare_data_for_answer(data):  
    user_response = get_message(data).lower()
    answer = ""
    tmp = trivia(user_response)
    if(user_response=='danke dir' or user_response=='danke' ):
        answer = "Gerne.."
    elif tmp!=None:
        answer = tmp
    else:
        answer = response1(user_response)
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