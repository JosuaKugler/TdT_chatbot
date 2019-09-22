from ahelper import say, recSpeech, alert, react, diss

from math import sqrt
from random import randint, choice
from time import sleep

def primzahl(zahl):
    for i in range(2, int(sqrt(zahl))):
        if zahl % i == 0:
            return False
    return True
        
playing = True
punkte = 0

satzteile = [["Dein", "Mein"],
            ["Kater", "Pizzalieferant"],
            ["versklavt", "bespringt"],
            ["meinen", "deinen"],
            ["Vater", "Zuhälter"],
            ["indem er", "indem er"],
            ["grüne", "verwesende"],
            ["Zombies", "Jediritter"],
            ["tötet", "ausbildet"]]

satz = ""

say("Wie heißt du?")
name = recSpeech()
react(name)
name = name.replace("ich ", "").replace("heiße ", "")

say("Hallo " + name)
diss()

for runde in range(len(satzteile)):
    zahl = randint(100, 1000) * 2 + 1
    
    invalidInput = True
    while invalidInput:
        say("Isst " + str(zahl) + " eine Primzahl?")
        eingabe = recSpeech()
        
        if eingabe in ["ja", "nein"]:
            invalidInput = False
        else:
            react(eingabe)
            say("Ach " + name + "Sag einfach Ja oder nein, so schwer ist das nicht ")
            diss()
    
    if eingabe == "ja" and primzahl(zahl) or eingabe == "nein" and not primzahl(zahl):
        punkte += 1
        satz += " " + satzteile[runde][0]
        say("Richtig! Du hast " + str(punkte) + " Punkte")
    else:
        punkte -= 1
        satz += " " + satzteile[runde][1]
        say("Falsch! Du hast leider nur noch " + str(punkte) + " Punkte")
        diss()

say(satz)