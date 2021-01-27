"""
Simple Flask app to run our text comparison pipeline 
as a POST endpoint.
"""

from flask import Flask
from flask import request
from flask import make_response
import json
import logging

from config_mgr import ConfigMgr
from text_processor import derive_core_words
from text_processor import compare_texts

#
# set up static data for all requests
#
app = Flask(__name__)
cfg = ConfigMgr(config_src='config/config.json')
stop_words = cfg.get('STOPWORDS')

logging.info(f'Flask app started.')


@app.route('/', methods=['POST'])
def text_compare():
    """ Our app accepts ANY post request on the published URL,
    but tests for proper keys in the JSON payload denoting texts
    to compare; otherwise, we issue a 400.
    Args:
        None
    Returns:
        comparison score from comarping the two texts
    """
    data = request.get_data()
    data = json.loads(data)

    if 'text1' not in data or 'text2' not in data:
        logging.critical('bad payload data - doc texts not specified')
        return 'Bad payload data - doc texts not specified', 400

    doc1 = data['text1']
    doc2 = data['text2']

    # get core words - remove stop words and punctuation
    doc1_words = derive_core_words(doc1, stop_words)
    doc2_words = derive_core_words(doc2, stop_words)

    # run comparison metrics on the words of the two texts
    score = compare_texts(cfg, doc1_words, doc2_words)
    ret_str = 'Test comparison score is {}\n'.format(score)

    response = make_response(ret_str)

    return response


if __name__ == '__main__':
    app.run()
