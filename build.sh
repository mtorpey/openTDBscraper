#!/bin/bash

echo "Scraping website..."
python3 download.py

CATEGORY_FILES=$(ls [0-9]*.lua | sort -n)
echo "Category files found: $CATEGORY_FILES"

echo "Producing TriviaQuestions.lua ..."
cat header.lua categories.lua $CATEGORY_FILES > TriviaBotQuizOpenTDB/TriviaQuestions.lua

# Clean up intermediate files
echo "Cleaning up intermediate files..."
rm $CATEGORY_FILES categories.lua
