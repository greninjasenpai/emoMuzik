import json
from pprint import pprint

with open('data.json') as f:
    data = json.load(f)

def get_max_emotion(data):
    dict1=data[0]["faceAttributes"]["emotion"]

    max=0
    max_emotion=""
    for item in dict1:
        confideance=dict1[item]
        if confideance>max:
            if item=="neutral":
                if confideance>0.8:
                    max_emotion=item
                    max=confideance
            else:
                max_emotion=item
                max=confideance
            

print(max_emotion)
