"""
driver.py

Main driver code for running, processing, and testing.
1) Check environment variables
2) Instantiate a ConfigMgr object to fetch config, including:
    - stop words for text processing
    - data file path
3) Ingest text from each file into doc variable
4) Derive core words from each doc
5) Run comparison scoring function on the two sets of core words
    and log results, as well as emit to standard error (console)
"""

import sys
import logging
from config_mgr import ConfigMgr
from text_processor import ingest_text
from text_processor import derive_core_words
from text_processor import compare_texts


def main(file1, file2, config_src=None):
    """ Main routine drives the work.
    Args:       
        file1 and file2: filename strings
        config_src: location of configuration
    Returns:    Zero for success; -1 for exception (for external callers)
    """
    cfg = ConfigMgr(config_src)
    logging.info('Driver: About to ingest and process texts.')

    try:
        stop_words = cfg.get('STOPWORDS')
        data_path = cfg.get('DATA_DIR')

        # ingest text from each file
        doc1 = ingest_text(data_path + '/' + file1)
        doc2 = ingest_text(data_path + '/' + file2)

        # get core words - remove stop words and punctuation
        doc1_words = derive_core_words(doc1, stop_words)
        doc2_words = derive_core_words(doc2, stop_words)

        # run comparison metrics on the words of the two texts
        score = compare_texts(cfg, doc1_words, doc2_words)
        logging.info(f'text comparison score:  {score}')
        sys.stderr.write(f'text comparison score:  {score}\n')
        sys.stderr.flush()

    except Exception as e:
        logging.critical(f'Process failure - exception:  {e}')
        sys.stderr.write(f'Process failure - exception:  {e}\n')
        sys.stderr.flush()
        exit(-1)

    # we've successfully concluded all processing so exit 0
    return 0


if __name__ == "__main__":
    # Quick sanity check on arguments. 
    # Note we should probably implement more robust arg
    # processing.
    if len(sys.argv) < 3:
        sys.stderr.write(f'usage: driver.py [file1] [file2]\n')
        sys.stderr.flush()
        sys.exit(-1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    ret_val = main(file1, file2, config_src='config/config.json')

    sys.exit(ret_val)
