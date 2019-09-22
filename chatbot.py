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
engine = pyttsx3.init()
isPlayingPrimesGame = False

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
#nltk.download('popular', quiet=True)

# # Für den ersten Start, ansonsten auskommentieren
#nltk.download('punkt')
#nltk.download('wordnet')


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
def response(user_response):
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
    #robo_response="TFIDX["+str(round(req_tfidf,2))+"]"
    robo_response=""
    if(req_tfidf==0):

        robo_response=robo_response+ "I beg your pardon, asshole? Did you mean \'Gong's theorem\'?"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

def colorprint(msg):
    print(colored("TRUMP: ", 'red', attrs=['bold']) + colored(msg, 'cyan'))

def prime(number):
    for i in range(2, int(math.sqrt(number))):
        if number % i == 0:
            return False
    return True

'''
Ausgabe
(Um die Konsolenausgabe übersichtlicher zu gestalten wird die Bibliothek termcolor benutzt)
'''
flag=True
clear = lambda: os.system('clear')
clear()
print(colored("TRUMP: ", 'red', attrs=['bold']) + colored("\tHello, my name is TRUMP. I'm an artificial Stupidity. Just ask me and I will give you a trumpy response!\n\tTo quit just type 'Bye'.", 'cyan'))
while(flag==True):
    while isPlayingPrimesGame == True:
        #number = random.randint(100, 1000) * 2 + 1
        e = random.randint(0,1)
        if e==0:
            number = 101
            while prime(number):
                number = random.randint(100, 10000)* 2 + 1
        else:
            number = 100
            while not prime(number):
                number = random.randint(100, 10000)* 2 + 1

        invalidInput = True
        while invalidInput:
            colorprint("Is " + str(number) + " a prime number?")
            inputTxt = input()

            if inputTxt in ["yes", "no", "exit"]:
                invalidInput = False
            else:
                t = trivia(inputTxt)
                if t != None: colorprint(trivia(inputTxt))
                colorprint("C'mon, just say yes or no, it's not *that* hard...")
                colorprint(random.choice(INDIGNITY_INPUTS))

        if inputTxt == "exit":
            isPlayingPrimesGame = False
            colorprint("OK, I've stopped the prime number game.")
        elif inputTxt == "yes" and prime(number) or inputTxt == "no" and not prime(number):
            points += 1
            colorprint("Correct! Your score is " + str(points) + ".")
        else:
            points -= 1
            colorprint("Wrong! Your score is " + str(points) + ".")
            colorprint(random.choice(INDIGNITY_RESPONSES))

    user_response = input()
    user_response=user_response.lower()
    if(user_response == "prime number game"):
        colorprint("OK, let's play the prime number game!")
        isPlayingPrimesGame = True
        points = 0
    elif(user_response!='bye'):
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
            engine.say(tmp)
            engine.runAndWait()
        else:
            print(colored("TRUMP: ", 'red', attrs=['bold']), end="")
            thisresponse = response(user_response)
            print(colored(thisresponse, 'cyan'))
            engine.say(thisresponse)
            engine.runAndWait()
            sent_tokens.remove(user_response)
    else:
        flag=False
        print(colored("TRUMP: ", 'red', attrs=['bold']) + colored("Bye! Make America great again!", 'cyan'))
