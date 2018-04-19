#! /usr/bin/python3

import json
from urllib.request import urlopen
from random import shuffle

# Generate a token
response = urlopen("https://opentdb.com/api_token.php?command=request")
html = response.read()
token = json.loads(html)["token"]
print(token)

# Download the questions/answers
response = urlopen('https://opentdb.com/api.php?amount=5&category=23' + "&token=" + token)
html = response.read()
questions = json.loads(html)["results"]

#for question in questions:
#    #print(question)
#    if question["type"] == "boolean":
#        print("True or false?")
#    else:
#        print("Multiple choice question:")
#    print(question["question"])
#    print(question["correct_answer"])
#    if question["type"] == "multiple":
#        for answer in question["incorrect_answers"]:
#            print(answer)
#    print("\n")


for q in questions:
    line = ""
    if q["type"] == "boolean":
        line += "True or False\n"
        line += q["question"]
    else:
        line += q["question"] + "\t"
        answers = [q["correct_answer"]] + q["incorrect_answers"]
        shuffle(answers)
        for answer in answers:
            line += "\n" + answer
    line += "\n\tAnswer: " + q["correct_answer"]
    print(line, "\n")
