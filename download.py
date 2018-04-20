#! /usr/bin/python3

import json
import os
from urllib.request import urlopen
from random import shuffle
from math import floor
from multiprocessing import Pool


# nb_questions = 1000
nb_questions_per_batches = 50
# nb_batches = floor(nb_questions / nb_questions_per_batches)

# Get the list of all categories
response = urlopen("https://opentdb.com/api_category.php")
html = response.read()
categories = json.loads(html)["trivia_categories"]

# Generate a token
response = urlopen("https://opentdb.com/api_token.php?command=request")
html = response.read()
session_token = json.loads(html)["token"]
print("Using session token: " + session_token)


def download_category(category, token=session_token):
    print("Working on category %d" % category["id"])

    # Get the number of questions for this category
    response = urlopen("https://opentdb.com/api_count.php?category=%d"\
         % category["id"])
    html = response.read()
    nb_questions = json.loads(html)["category_question_count"]["total_question_count"]

    # Calculate the number of batches and the number of remaining questions
    nb_batches = floor(nb_questions / nb_questions_per_batches)
    remaining_questions = nb_questions % nb_questions_per_batches

    # Create the request URL
    sourceurl = 'https://opentdb.com/api.php?amount=%d&category=%d&token=%s'\
         % (nb_questions_per_batches, category["id"], token)

    # Create the category file
    category_name = category["name"]
    filename = "%s.csv" % category_name
    file = open(filename, "w")

    # Loop on the number of batches wanted
    for i in range(nb_batches):
        print("Downloading questions %d-%d out of %d for category %d (%s)"\
            % (i*nb_questions_per_batches + 1, (i+1)*nb_questions_per_batches, nb_questions,\
                category["id"], category_name))
        # Download the questions/answers
        response = urlopen(sourceurl)
        html = response.read()
        questions = json.loads(html)["results"]
        if questions:
            # Process the questions/answers
            for q in questions:
                line = ""
                if q["type"] == "boolean":
                    line += q["question"].replace(";", '') + ";" + "True or false?"
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

    # Create the URL for the remaining questions
    sourceurl = 'https://opentdb.com/api.php?amount=%d&category=%d&token=%s'\
        % (remaining_questions, category["id"], token)
    print("Downloading questions %d-%d out of %d for category %d (%s)"\
        % (nb_questions - remaining_questions + 1, nb_questions, nb_questions,\
            category["id"], category_name))
    # Download the questions/answers
    response = urlopen(sourceurl)
    html = response.read()
    questions = json.loads(html)["results"]
    # Process the questions/answers
    for q in questions:
        line = ""
        if q["type"] == "boolean":
            line += q["question"].replace(";", '') + ";" + "True or false?" 
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


if __name__ == "__main__":
    nbProcesses = len(categories)
    with Pool(nbProcesses) as p:
        p.map(download_category, categories)