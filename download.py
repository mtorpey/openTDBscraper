#! /usr/bin/python3

import json
from urllib.request import urlopen
from random import shuffle
from math import floor


nbQuestions = 250
nbBatches = floor(nbQuestions / 50)
categories = [e for e in range(50)]

# Generate a token
response = urlopen("https://opentdb.com/api_token.php?command=request")
html = response.read()
token = json.loads(html)["token"]
print("Using session token: " + token)

# Loop on every category
for category in categories:
    print("\nWorking on category %d" % category)
    sourceurl = 'https://opentdb.com/api.php?amount=50&category=' + str(category)
    file = open("questions%d.csv" % category, "w")

    # Loop on the number of batches wanted
    for i in range(nbBatches):
        print("Downloading questions %d-%d out of %d" % (i*50, (i+1)*50, nbQuestions))
        # Download the questions/answers
        response = urlopen(sourceurl + "&token=" + token)
        html = response.read()
        questions = json.loads(html)["results"]

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
    file.close()
