import androidhelper
from random import choice, randint
import sys

droid = androidhelper.Android()

def ranelem(liste):
    r = randint(0, len(liste)-1)
    return liste[r]

def say(text):
    droid.ttsSpeak("¡" + text)
    while droid.ttsIsSpeaking().result: pass

def alert(title="", msg=""):
    return droid.dialogGetInput(title, msg).result

abortKeywords = ["stopp", "stop"]

def recSpeech(msg=""):
    res = droid.recognizeSpeech(msg, "German").result
    if res != None:
        res = res.lower()
        for a in abortKeywords:
            while a in res:
                s = res.find(a)
                res = res[s + len(a):].lstrip()
        
        return res
    else:        
        return ""

backdisses = ["Noch so ein Ton, Intensivstation!",
            "Noch so ein Gelalle, Leichenhalle!",
            "Noch so ein Spruch, Kieferbruch!",
            "Noch so ne Tat, Rollstuhlfahrt!",
            "Noch so ein Wort, Zähne fort!",
            "Noch so ein Akt, Kopf zerhackt!",
            "Noch so ein Furz, Treppensturz!",
            "Noch so ein Gägg, Zähne wegg!"]

def backdiss():
    say(ranelem(backdisses))

def react(eingabe):
    if "deine mudda" in eingabe or "deine mutter" in eingabe:
        backdiss()
    if "grün" in eingabe:
        say("Ich bin tot!")
    if "neonschwarz" in eingabe:
    	say("Ach wie schön!")
    if "echo" in eingabe:
        say("echoechoechoechoecho")
    if "vielleicht" in eingabe:
        say("Entscheide dich. Oder ich entscheide für dich.")
    if "halt die klappe" in eingabe or "halt die fresse" in eingabe or "halts maul" in eingabe or "halt's maul" in eingabe:
        backdiss()
        sys.exit()
    if "app beenden" in eingabe:
        sys.exit()

def setVol(vol):
    droid.setMediaVolume(vol)
    
anreden = ["wende lang wärst wiede doof bist würdste knieend aus der dachrinne saufen",
            "und schau nicht wie ein auto mit standlicht",
            "deine mudda",
            "Herzlichen Glückwunsch! Du darfst dich jetzt mit der Titanic darum streiten, wer tiefer gesunken ist.",
            "Du bist wie ein Q: Eine Null mit einem kleinen Schwanz",
            "Du bist so hässlich, dich kann man mit Paint malen.",
            "Du hast aber ganz schön viel Meinung für so wenig Ahnung.",
            "Wisch dir mal den Mund, da sind noch Reste von der Scheiße, die du gerade gelabert hast.",
            "Dank dir weiß ich es jetzt Stille zu schätzen.",
            "Wenn du eine Fliege verschluckst, hast du mehr Gehirn im Bauch als im Kopf",
			"Ich wollte gerade Frikadellen machen, kannst du mir deine Hackfresse leihen?"]

def diss():
    say(ranelem(anreden))
    
def evalSpeech(txt):
    zeichen = {"x": "", "mal": "", "hoch": "**", "geteilt durch": "/", "durch": "/", "was ist": ""}
    
    for i in zeichen.keys():
        txt = txt.replace(i, zeichen[i])
    
    for i in range(len(txt)):
        if txt[i].isalpha(): txt = txt[:i] + " " + txt[i+1:]
        
    try:
        return eval(txt)
    except:
        return ""

def speechNum(n):
    try:
        if str(n) in (str(float(n)), str(int(n))):
            n = float(n)
            if float(int(n)) == n:
                return str(int(n))
            else:
                return str(n).replace(".", ",")
    except:
        return "trölf"