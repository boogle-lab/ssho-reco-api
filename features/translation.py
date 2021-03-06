import requests
# import json
# import time
# from datetime import datetime

import re
from google_trans_new import google_translator

from nltk.stem import WordNetLemmatizer
import nltk
nltk.download("wordnet")

URL = "http://api.ssho.tech:8080/item"

def toEng(title):
    lem = WordNetLemmatizer()
    title = cleanTitle(title)

    translator = google_translator()
    title = translator.translate(title, lang_tgt="en")

    title = [lem.lemmatize(w).lower() for w in title.split()]
    return ' '.join(title)

def clean(my_dict):
    try:
        del my_dict['productExtra']
        del my_dict['imageUrl']
        del my_dict['link']

    except KeyError:
        pass
    return my_dict

def getItems():
    response = requests.get(URL)
    items = response.json()
    items = [clean(x) for x in items]
    return items

def cleanTitle(text):
    text = re.sub(" /.+$| \\[.+\\]| [A-Z]+? \\[.+\\]|^[A-Za-z]+[0-9]+? | -.+$", "", text)
    # remove punctuations
    text = re.sub(r"[^\w\s]", "", text)
    return text

def transItem(title):
    return toEng(cleanTitle(title))

# def finalItems(file = None):
#     date = str(datetime.now().strftime("%y%m%d"))
#     if file==None:
#         items = getItems()
#         with open("processed_{}.json".format(date), "w") as f:
#             json.dump(items, f, ensure_ascii=False)
#     else:
#         with open(file, "r") as f:
#             items = json.load(f)
#
#     for i in range(len(items)):
#         # items[i]['_title'] = cleanTitle(items[i]['title'])
#         print("==== itemId : {}, count : {}".format(items[i]['id'], i+1))
#         print("Original title : ", items[i]['title'])
#         new = toEng(items[i]['title'])
#         print("Translated : ", new)
#         items[i]['translated'] = new
#         print()
#
#     with open("translated_{}.json".format(date), "w") as f:
#         json.dump(items, f, ensure_ascii=False)
#
#     return items

if __name__=="__main__":
    sample = {"id": "0001221668",
              "category": "탑",
              "mallNo": "0001",
              "mallNm": "스타일난다",
              "title": "미니메시 오프숄더 스모크",
              "price": "29000",
              "tagList": [{"id": "fc894811d7454cd89ba0f2c21b91d942", "name": "캐주얼"},
                          {"id": "990f3147a4544a05aaa5fd1abb095312", "name": "가을"}]}

    out = transItem(sample)
    print("original : ", out['title'])
    print("translated out : ", out['translated'])