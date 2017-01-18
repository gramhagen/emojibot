# -*- coding: utf-8 -*-
"""Base Response object"""

import logging

from abc import ABCMeta, abstractmethod, abstractproperty


class Response(object):
    """Base Response class to extend

    Properties:
        api_method (str): slack api method to call
        channel (str): slack channel to send response to
    """

    __metaclass__ = ABCMeta

    channel = None

    @abstractproperty
    def api_method(self):
        """Slack api method to call"""

        raise NotImplementedError

    def __init__(self, channel):
        """Constructor

        Args:
            channel (str): channel to send response to
        """

        self.channel = channel

    @abstractmethod
    def to_dict(self):
        """Represent arguments for api call as a dict"""

        raise NotImplementedError

    def send(self, client):
        """Send response to slack

        Args:
            client (SlackClient): slack client
        """

        logging.debug('Received %s response: %s', type(self).__name__, self)

        try:
            client.api_call(self.api_method, **self.to_dict())
        except Exception as e:
            logging.error('Error sending response: %s, %s', self, e, exc_info=True)
