# openTDBscraper
Scraper for the website OpenTDB (https://opentdb.com) aimed at creating Anki trivia flashcards

To run the scaper, execute `python3 download.py` from a terminal.

The script will automatically download every trivia category from openTDB, creating one CSV file per category. Empty category files will automatically be deleted.

# Required libraries

* os
* json
* urllib
* random
* math
* mutliprocessing
