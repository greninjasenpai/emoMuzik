import json
from pprint import pprint

with open('data.json') as f:
    data = json.load(f)
dict1=data[0]["faceAttributes"]["emotion"]
#sadness=data[0]["faceAttributes"]["emotion"]["sadness"]
#anger=data[0]["faceAttributes"]["emotion"]["anger"]
#contempt=data[0]["faceAttributes"]["emotion"]["contempt"]
#disgust=data[0]["faceAttributes"]["emotion"]["disgust"]
#fear=data[0]["faceAttributes"]["emotion"]["fear"]
#happiness=data[0]["faceAttributes"]["emotion"]["happiness"]
#neutral=data[0]["faceAttributes"]["emotion"]["neutral"]
#surprise=data[0]["faceAttributes"]["emotion"]["surprise"]

sorted_dict=sorted(dict1.items(), key=lambda kv: kv[1],reverse=True)

pprint(sorted_dict)
#first2pairs = {k: mydict[k] for k in sorted(mydict.keys())[:2]}