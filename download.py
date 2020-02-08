#! /usr/bin/python3

import json
import os
from urllib.request import urlopen
from random import shuffle
from math import floor
from multiprocessing import Pool
from html import unescape


nb_questions_per_batch = 50

nb_questions_written = 0

# Get the list of all categories
response = urlopen("https://opentdb.com/api_category.php")
html = response.read()
categories = json.loads(html)["trivia_categories"]

# Find out about each category
print("CATEGORIES:")
for category in categories:
    response = urlopen("https://opentdb.com/api_count.php?category=%d" % category["id"])
    html = response.read()
    nb_questions = json.loads(html)["category_question_count"]["total_question_count"]
    category["nb_questions"] = nb_questions
    print("%d %s (%d questions)" % (category["id"], category["name"], nb_questions))

# Generate a token
response = urlopen("https://opentdb.com/api_token.php?command=request")
html = response.read()
session_token = json.loads(html)["token"]
print("Using session token: " + session_token)


def download_category(category, token=session_token):
    category_id = category["id"]

    # Calculate the number of batches and the number of remaining questions
    nb_questions = category["nb_questions"]
    nr_batches = floor(nb_questions / nb_questions_per_batch)
    remaining_questions = nb_questions % nb_questions_per_batch

    # Accumulate questions
    questions = []

    # Full-size batches
    for i in range(nr_batches):
        print("Category %d: %d/%d" % (category_id, i + 1, nr_batches + 1))
        questions += next_batch(nb_questions_per_batch, category_id, token)

    # Last few questions
    print("Category %d: %d/%d" % (category_id, nr_batches + 1, nr_batches + 1))
    questions += next_batch(remaining_questions, category_id, token)

    category["questions"] = questions

    return category


def next_batch(nb_questions, category_id, token):
    # Create the request URL
    sourceurl = "https://opentdb.com/api.php?amount=%d&category=%d&token=%s" % (
        nb_questions,
        category_id,
        token,
    )

    # Download the questions/answers
    response = urlopen(sourceurl)
    html = response.read()
    return json.loads(html)["results"]


def write_categories(filename, categories):
    file = open(filename, "w")
    for category in categories:
        file.write(
            "TriviaBot_Questions[1]['Categories'][%d] = \"%s\";\n"
            % (category["id"], category["name"])
        )
    file.write("\n")
    file.close()


def write_questions(category):
    # Get the components we need
    category_id = category["id"]
    questions = category["questions"]
    global nb_questions_written

    # Create the category file
    filename = "%d.lua" % category_id
    file = open(filename, "w")

    for q in questions:
        if q["type"] != "boolean":  # skip all true/false questions
            nb_questions_written += 1
            out_dict = {
                "Question": "[[" + unescape(q["question"]) + "]]",
                "Answers": "{[[" + unescape(q["correct_answer"]) + "]]}",
                "Category": str(category_id),
                "Points": difficulty_to_points(q["difficulty"]),
                "Hints": "{[[%s]]}" % (options_string(q)),
            }
            for k, v in out_dict.items():
                file.write(
                    "TriviaBot_Questions[1]['%s'][%d] = %s;\n"
                    % (k, nb_questions_written, v)
                )
            file.write("\n")
    file.close


def options_string(question):
    o = question["incorrect_answers"]
    o.append(question["correct_answer"])
    assert len(o) == 4
    shuffle(o)
    o = list(map(unescape, o))
    return "OPTIONS: %s; %s; %s; %s" % (o[0], o[1], o[2], o[3])


def difficulty_to_points(string):
    if string == "easy":
        return 1
    elif string == "medium":
        return 2
    elif string == "hard":
        return 3
    raise Exception("Invalid difficulty: " + string)


if __name__ == "__main__":
    #categories = [categories[0], categories[1], categories[2]]  # for testing
    write_categories("categories.lua", categories)
    nbProcesses = len(categories)
    with Pool(nbProcesses) as p:
        categories = list(p.map(download_category, categories))

    # Write the questions/answers
    for category in categories:
        write_questions(category)
