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
GREETING_INPUTS = ("hello", "hi")
GREETING_RESPONSES = ["Make America Great Again!!!", "Part of my beauty is that I am very rich!", "hi", "hey", "what's up", "Good afternoon", "hello", "It's nice meet you", "Make America Great Again!!!", "Part of my beauty is that I am very rich!"]

# Beleidigungen
INDIGNITY_INPUTS = ("motherfucker", "bitch", "cunt", "robot", "bot", "nigga", "stupid", "asshole", "fuck")
INDIGNITY_RESPONSES = ["You're fired", "We gonna build a wall around you", "Fake News", "You are like Obama", "Mexicunt", "Stupid European", "Bitch"]

# Komplimente
COMPLIMENT_INPUTS = ("nice", "sexy", "clever", "humanoid", "talented", "trumpy")
COMPLIMENT_RESPONSES = ["thanks", "You too", "You're almost as amazing as Trump"]

# Reaktionen
REACTION_INPUTS = [GREETING_INPUTS, INDIGNITY_INPUTS, COMPLIMENT_INPUTS]
REACTION_RESPONSES = [GREETING_RESPONSES, INDIGNITY_RESPONSES, COMPLIMENT_RESPONSES]

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
    '''Wenn die Nutzereingabe ien Begrüßung ist, Antwortet der Bot mit einer zufälligen Begrüßung als Antwort,
    gleiches gilt für Beleidigungen'''
    for word in sentence.split():
        for reaction in range(len(REACTION_INPUTS)):
            if word.lower() in REACTION_INPUTS[reaction]:
                return random.choice(REACTION_RESPONSES[reaction])

# Antwort Erzeugung
def response(user_response):
    stop_words = get_stop_words('english')
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=stop_words,ngram_range=(1, 10))
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

'''
Ausgabe
(Um die Konsolenausgabe übersichtlicher zu gestalten wird die Bibliothek termcolor benutzt)
'''
flag=True
clear = lambda: os.system('clear')
clear()
print(colored("TRUMP: ", 'red', attrs=['bold']) + colored("\tHello, my name is TRUMP. I'm an artificial Stupidity. Just ask me and I will give you a trumpy response!\n\tTo quit just type 'Bye'.", 'cyan'))
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if user_response == "satz von gong":
            cols = ['cyan', 'green', 'red', 'blue', 'yellow', 'grey', 'white', 'magenta']
            for i in range(random.randint(42,420)):
                print(colored("Satz von Gong", cols[random.randint(0,len(cols)-1)]))
        tmp = trivia(user_response)
        if(user_response=='danke dir' or user_response=='danke' ):
            flag=False
            print(colored("TRUMP: ", 'red', attrs=['bold']) + colored( "Gerne..", 'cyan'))
        elif tmp!=None:
            print(colored("TRUMP: ", 'red', attrs=['bold']) + colored(tmp, 'cyan'))
        else:
            print(colored("TRUMP: ", 'red', attrs=['bold']), end="")
            print(colored(response(user_response), 'cyan'))
            sent_tokens.remove(user_response)
    else:
        flag=False
        print(colored("TRUMP: ", 'red', attrs=['bold']) + colored("Satz von Gong! Tschüss! Mach's gut. Satz von Gong!", 'cyan'))
