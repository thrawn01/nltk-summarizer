
## Wat dis?
A WSGI Middleware that runs HTML documents through a text summarizer if
the path ends in .tldr

Attempts to summarize the HTML document by searching for frequently
occuring words and selecting the sentence with the highest frequency of
common words as the summary.

This project was an experiment to play around the NLTK

## Setup
```
# Ubuntu 11.04
sudo apt-get install build-essential libevent-dev libyaml-dev

# Python Package isolation
virtualenv --no-site-packages .
source bin/activate

# gevent wsgi server is needed by unit tests
pip install nose webob nltk gevent

# Get the word files for NLTK
./get_words.py

# Run unit tests from the project root directory
nosetests
```
