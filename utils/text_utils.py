""""Container class for all shared text processing utilities"""

import re
import string

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem.lancaster import LancasterStemmer


tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
stop_words = set(stopwords.words('english') + list(string.punctuation))

stemmer = LancasterStemmer()

regex_link = r'https?:\/\/.*\/\w*'
regex_ticker = r'\$\w*'
regex_punc = r'[{}]'.format(string.punctuation)

# TODO: consider keeping/handling punctuation (and emoticons)


def valid_string(word):
    """Remove punctuation, stop words, and small words"""

    if word in stop_words:
        # remove stop words or punctuations
        return False
    if len(word) <= 2:
        # remove empty or very small words
        return False
    return True


def process_sentence(sentence):
    """Remove links, tickers, and tokenize sentence"""

    # remove links
    sentence = re.sub(regex_link, '', sentence)
    # remove tickers
    sentence = re.sub(regex_ticker, '', sentence)
    return tokenizer.tokenize(sentence.lower())


def process_word(word):
    """Remove all punctuation and stem words"""
    word = re.sub(regex_punc, '', word)
    return stemmer.stem(word)


def clean_sentence(sentence):
    """Clean a sentence by processesing and reforming all the words in it"""

    return ' '.join([process_word(word) for word in process_sentence(sentence) if valid_string(word)])


def encode_sentence(sentence, vocab):
    """Encode words -> ids in a sentence using a vocabulary lookup"""

    return [vocab[word] for word in sentence.split() if word in vocab]
