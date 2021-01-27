"""
Draft code to process text
"""

import logging
import string
import re
import sys


def derive_core_words(text, stopwords):
    """ Given a list of stop words, extract all other
    "important" words from a given text document.
    Args:
        text:   string containing entire text document to process
        stopwords:  list of stop words (from NLTK English stop words set)
    Returns:    
        core_word_list: List of core words in doc
    """
    punc_pat = re.compile(r'[' + string.punctuation + ']') 
    core_word_list = [] 
    for word in text.split():
        word = word.lower()
        word = punc_pat.sub('', word)
        if word not in stopwords:
            core_word_list.append(word)
    return core_word_list


def compare_texts(cfg, text1, text2):
    """ Do the work of comparing two texts. This function delegates
    to a configurable function to do the work, dynamically fetching
    the function at runtime.
    Args:
        cfg:    ConfigMgr object, to use to fetch function name
        text1 & text2:  text lists to pass to the comparison function
    """
    # get comparison function name from config
    comp_func_name = cfg.get('COMP_FUNCTION')
    # get our current module name
    cur_module = sys.modules[__name__]
    # fetch function object from module
    comparison_func = getattr(cur_module, comp_func_name)

    # do the real work
    return comparison_func(text1, text2)


def ingest_text(file_src):
    """ Ingest text from a given filename.
    Args:
        file_src:   string representing file path
    Returns:
        buffer containing text
    """
    buf = ''
    with open(file_src, 'r') as text_file:
        buf = text_file.read()
    return buf.strip()


def get_jaccard_sim(words1, words2):
    """
    Implement the NLP Jaccard similarity score, which
    defines the similarity of two texts as the quotient 
    of their intersection and their union.
    Args:
        words1: list of words comprising first text
        words2: list of words comprising second text
    Returns:
        Rounded (4 places) Jaccard score 

    """

    # get unique words only, then do set operations
    a = set(words1)
    b = set(words2)
    c = a.intersection(b)

    score = round(float(len(c)) / (len(a) + len(b) - len(c)), 4)

    logging.info(f'comparison score: {score} | words in common: {c} | num unique words: {len(a) + len(b) - len(c)}')
    return score