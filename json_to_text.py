import json
from os import listdir
from os.path import isfile, join


PATH = "json"
trump_data_file = open(join(PATH,"trump_data_file.txt"),"w")
onlyfiles = [f for f in listdir(PATH) if isfile(join(PATH, f)) and f[-4:] == "json"]
print(onlyfiles)
for file in onlyfiles:
    print("NEW FILE ",file)
    print("*"*100)
    with open(join(PATH,file)) as f:
        json_data = json.load(f)
        for tweet in json_data:
            text = tweet["text"]
            print(text)
            trump_data_file.write(text+"\n\n")


trump_data_file.close()
# with open('trump_fake_news.json') as json_data:
#   d = json.load(json_data)