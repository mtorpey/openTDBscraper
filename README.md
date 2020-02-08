# openTDBscraper
Scraper for the website [OpenTDB](https://opentdb.com), modified from the
original by AdrienCos, and now outputting a WoW Classic TriviaBot addon

To run the scaper, execute `./build.sh` from a terminal.

The script will automatically download every trivia category from openTDB, and
output a completed TriviaBot quiz addon in the `TriviaBotQuizOpenTDB/`
directory.

# Required libraries

* os
* json
* urllib
* random
* math
* mutliprocessing
* html

# Credits

[OpenTriviaDB](https://opentdb.com/) questions by [PIXELTAIL GAMES LLC](http://www.pixeltailgames.com/) are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Thanks also to AdrienCos, who made the original version of this for Anki
flashcards: https://github.com/AdrienCos/openTDBscraper
