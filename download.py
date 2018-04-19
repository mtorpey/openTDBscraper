#! /usr/bin/python3

import json
import os
from urllib.request import urlopen
from random import shuffle
from math import floor
from multiprocessing import Pool


nbQuestions = 2000
nbBatches = floor(nbQuestions / 50)
categories = [e for e in range(1,33)]

# Generate a token
response = urlopen("https://opentdb.com/api_token.php?command=request")
html = response.read()
session_token = json.loads(html)["token"]
print("Using session token: " + session_token)


def download_category(category, token=session_token):
    print("Working on category %d" % category)
    sourceurl = 'https://opentdb.com/api.php?amount=50&category='\
         + str(category) + "&token=" + token
    file = open("questions%d.csv" % category, "w")
    nbLines = 0

    # Loop on the number of batches wanted
    for i in range(nbBatches):
        print("Downloading questions %d-%d out of %d for category %d"\
             % (i*50, (i+1)*50, nbQuestions, category))
        # Download the questions/answers
        response = urlopen(sourceurl)
        html = response.read()
        questions = json.loads(html)["results"]

        if questions:
            # Process the questions/answers
            for q in questions:
                line = ""
                if q["type"] == "boolean":
                    line += "True or false?" + ";" + q["question"].replace(";", '')
                else:
                    line += q["question"].replace(";", '') + ";"
                    answers = [q["correct_answer"]] + q["incorrect_answers"]
                    shuffle(answers)
                    for answer in answers:
                        line += answer.replace(";", '') + "<br>"
                    line = line[:-4]
                line += ";" + q["correct_answer"].replace(";", '') + "\n"
                file.write(line)
                nbLines += 1
        else: 
            break
    file.close()
    if nbLines == 0:
        os.remove("questions%d.csv" % category)

if __name__ == "__main__":
    with Pool(len(categories)) as p:
        p.map(download_category, categories)