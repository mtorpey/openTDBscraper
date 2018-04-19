#! /usr/bin/python3

import json
import os
from urllib.request import urlopen
from random import shuffle
from math import floor
from multiprocessing import Pool


nbQuestions = 1000
nbQuestionsPerBatches = 20
nbBatches = floor(nbQuestions / nbQuestionsPerBatches)
categories = [e for e in range(1,33)]

# Generate a token
response = urlopen("https://opentdb.com/api_token.php?command=request")
html = response.read()
session_token = json.loads(html)["token"]
print("Using session token: " + session_token)


def download_category(category, token=session_token):
    #TODO: Query https://opentdb.com/api_count.php?category=CATEGORY to get the number of questions for the category
    # and find the largest divisor of it under 50 to make sure we get all the questions
    print("Working on category %d" % category)
    # Get the category name
    categoryurl = 'https://opentdb.com/api.php?amount=1&category=%d' % category
    sourceurl = 'https://opentdb.com/api.php?amount=%d&category=%d&token=%s'\
         % (nbQuestionsPerBatches, category, token)
         
    response = urlopen(categoryurl)
    html = response.read()
    results = json.loads(html)["results"]
    if results:
        category_name = results[0]["category"]
        # Create the category file
        filename = "%s.csv" % category_name
        file = open(filename, "w")
        # Loop on the number of batches wanted
        for i in range(nbBatches):
            print("Downloading questions %d-%d out of %d for category %d (%s)"\
                % (i*nbQuestionsPerBatches, (i+1)*nbQuestionsPerBatches, nbQuestions,\
                 category, category_name))
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
            else: 
                # No more questions to download
                break
        file.close()

if __name__ == "__main__":
    nbProcesses = len(categories)
    with Pool(nbProcesses) as p:
        p.map(download_category, categories)