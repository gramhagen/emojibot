# -*- coding: utf-8 -*-
"""Emojify Command"""

import pickle

import tflearn

from tflearn.data_utils import pad_sequences

from emojibot.utils.reaction import Reaction
from emojibot.utils.text_utils import clean_sentence, encode_sentence


class Emojify(object):
    """Emojify Command class"""

    model = None
    sentence_length = None
    emoji_map = None
    label_map = None

    def __init__(self, config):
        """Constructor"""

        self.emoji_map = config['EMOJI_MAPPING']
        with open(config['DATA_PARAMS_PICKLE'], 'rb') as f:
            params = pickle.load(f)

        self.label_map = params['labels']
        self.vocab = params['vocab']
        self.max_sequence_length = params['max_sequence_length']

        num_words = len(self.vocab)
        num_classes = len(self.emoji_map)

        # match network to models/lstm.ipynb (with 0 dropout)
        net = tflearn.input_data([None, self.max_sequence_length])
        net = tflearn.embedding(net, input_dim=num_words, output_dim=128)
        net = tflearn.lstm(net, 128, dropout=0.)
        net = tflearn.fully_connected(net, num_classes, activation='softmax')
        net = tflearn.regression(net, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy')
        self.model = tflearn.DNN(net, tensorboard_verbose=0)

        self.model.load(config['EMOJI_MODEL_PATH'])

    def run(self, channel, text, timestamp):
        """Text

        Args:
            channel (str): slack channel of message
            text (str): text of message
            timestamp (float): timestamp of message
        Returns:
            (Response):
        """

        # clean text (remove handles, links, punctuation, stop words, and apply stemmer)
        text = clean_sentence(sentence=text)
        text = encode_sentence(sentence=text, vocab=self.vocab)
        sequence = pad_sequences([text], maxlen=self.max_sequence_length, value=0.)

        probs = self.model.predict(sequence)[0]
        emoji_class = probs.index(max(probs))
        emoji = self.emoji_map[self.label_map[emoji_class]]
        return Reaction(channel=channel, name=emoji, timestamp=timestamp)
