# Fetch
Data Engineer Coding Exercise

## Intro
This is a short coding project aimed at solving a challenge to compare
two texts and apply some kind of similarity metric, *without* using 
external libraries such as NLTK.

The simple program takes as input TWO (2) text document files (or text document
strings, if invoked via Flask - see below) and outputs (or returns) a simple
score between 0 and 1, with a higher score representing greater similarity
(see below for futher discussion).

## Running The Code
This project supports two functional modes:
1) Interactive run via the command line
2) Sending a JSON payload file via curl to a Flask endpoint

### Interactive Use
Note that the sample input texts as provided in the challenge have been 
saved in a *data* directory.

There are THREE (3) text samples:

sample1.txt

sample2.txt

sample3.txt

At the command line at the project root, run the following script:

$ ./run.sh sample1.txt sample2.txt

Note the script requires two arguments. You may of course denote different 
combinations of files (e.g., 1 and 3, 2 and 3), or create new ones, but the 
script will not run without two arguments denoting the two text files
to be compared.

A simple score will be written to your terminal's standard error/output.

### Flask-based Use
A small Flask app makes use of the same text comparison logic.

The Flask library must be imported. I suggest creating a virtual environment.
At the project root, execute on the command line:

$ python3 -m venv .venv

$ source .venv/bin/activate

You can now install the requirements:

$ pip install -r requirements.txt

You can now fire up the Flask app, via this script:

$ ./run_flask.sh

Flask will start a dev web server running (in the foreground) in your shell.
You can background the process, or navigate to a new terminal/shell and then run:

$ ./run_cli_payload1.sh

Which will invoke curl with a JSON payload file containing two text document strings.
Or you can likewise run:

$ ./run_cli_payload2.sh

For a different combination of text strings.  Note that the payload files "live" in
the data directory as well.

Note that running curl on the command line with a data payload of JSON text with 
embedded single quotes (e.g., '{"text1": "This is some text in which you'll find 
an embedded quote."}') requires that any single quote is escaped (e.g., "you'\''ll")
which is VERY ugly and VERY cumbersome. I have therefore stowed the payload data
away in files.

## Approach, Thoughts, and Considerations

### NLP
Having done some work with NLP I enjoyed the challenge, though of course we 
can't use any NLP-based libraries.  However, I took a standard NLP-based 
approach, which was to remove any and all punctuation, as well as remove 
so-called "stop words", or words that are so common, and so basically functional,
that they do not convey semantic significance. And although I could not use
NLTK, I could nevertheless retrieve the set of NLTK English stop words, and 
save it in configuration, to be used by my code.

I thereby collected all non-stop words from each text sample. As part of
some exploratory data analysis (EDA), I also recorded word frequencies
for each document, and noted for example that sample 1 and sample 2
have similar word frequencies.

However, instead of using word frequencies, I created sets of unique
words for each document, and then applied the simple Jaccard similarity score, 
which calculates the quotient of the intersection (words in common) by all
the words (union of both documents). Python's set methods make this quite 
simple and straightforward.  There are other NLP metrics for similarity, but
they require APIs which I couldn't use.

### Code Organization
With the exception of my use of a Config Mgr class to handle reading and
fetching config information, my code is very functional, and not object-oriented. 
With refined requirements and more concrete use cases, I could see
refactoring some of the code into classes.  For example, a more robust Flask
app could possibly benefit from more OO-based code for the text processing.

As noted, I deposited the text samples into separate files in a data directory.

A main driver module coordinates the main work of ingesting the designated
text files, deriving the core words (removing punctuation and stop words), 
and then invoking the comparison function.  The simple score is both
logged to the log file, as well as written out to the standard error.

Text processing, including ingestion, minor NLP processing (removing stop words),
and running a comparison function all happens in the text_processor module. 
This module is re-used by the Flask app.

Because the Jaccard score is but one way of measuring text similarity, I wanted
to allow for the easy exchange of new comparison functions. I therefore use some
minor Python meta-programming techniques to fetch the name of the comparison function 
from configuration, and then fetch the Python function object name from the runtime
namespace.  A new function can be written, dropped into the module file, and
the configuration changed, without having to change any other code, especially 
the client code in the driver module.

### Flask App
The Flask app is very bare bones, and does not even have a granular endpoint.
That is, any POST to its URL will hit the single text_compare() function and
initiate the processing. A more robust implementaiton would build the API out
further - this is very much a "quick and dirty" implementation, as proof-of-concept.







