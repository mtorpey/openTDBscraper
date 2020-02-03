#! /usr/bin/python3

import json
import os
from urllib.request import urlopen
from random import shuffle
from math import floor
from multiprocessing import Pool


nb_questions_per_batch = 50

# Get the list of all categories
response = urlopen("https://opentdb.com/api_category.php")
html = response.read()
categories = json.loads(html)["trivia_categories"]
print("Got the following categories:")
print(categories)

# Generate a token
response = urlopen("https://opentdb.com/api_token.php?command=request")
html = response.read()
session_token = json.loads(html)["token"]
print("Using session token: " + session_token)


def download_category(category, token=session_token):
    category_id = category["id"]
    print("Working on category %d" % category_id)

    # Get the number of questions for this category
    response = urlopen("https://opentdb.com/api_count.php?category=%d" % category_id)
    html = response.read()
    nb_questions = json.loads(html)["category_question_count"]["total_question_count"]

    # Calculate the number of batches and the number of remaining questions
    nr_batches = floor(nb_questions / nb_questions_per_batch)
    remaining_questions = nb_questions % nb_questions_per_batch

    # Accumulate questions
    questions = []

    # Full-size batches
    for i in range(nr_batches):
        print("Batch", i + 1, "of", nr_batches + 1, "in category", category_id)
        questions += next_batch(nb_questions_per_batch, category_id, token)

    # Last few questions
    print(
        "Batch", nr_batches + 1, "of", nr_batches + 1, "in category", category_id,
    )
    questions += next_batch(remaining_questions, category_id, token)

    # Process the questions/answers
    write_questions(category["id"], questions)


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


def write_questions(category_id, questions):
    # Create the category file
    filename = "%d.csv" % category_id
    file = open(filename, "w")

    count = 0
    for q in questions:
        if q["type"] != "boolean":  # skip all true/false questions
            count += 1
            out_dict = {
                "Question": '"' + q["question"] + '"',
                "Answers": '{"' + q["correct_answer"] + '"}',
                "Category": str(category_id),
                "Points": q["difficulty"],
                "Hints": "{}",
            }
            for k, v in out_dict.items():
                file.write("TriviaBot_Questions[2]['%s'][%d] = %s;\n" % (k, count, v))
            file.write("\n")
    file.close


if __name__ == "__main__":
    nbProcesses = len(categories)
    with Pool(nbProcesses) as p:
        p.map(download_category, categories)
