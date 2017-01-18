# -*- coding: utf-8 -*-
"""Message Class Container"""


class Message(object):
    """Message Class"""

    channel = None
    text = None
    timestamp = None
    user = None

    def __init__(self, **kwargs):
        """Constructor

        Args:
            kwargs (dict): keyword arguments
        """

        bot_ref = kwargs.get('bot_ref', '')

        self.channel = kwargs.get('channel')
        self.text = kwargs.get('text')[len(bot_ref):].strip(': ')
        self.timestamp = kwargs.get('ts')
        self.user = kwargs.get('user')

    def __repr__(self):
        """String representation of class"""

        output = 'Channel: {channel}, Text: {text}, Timestamp: {timestamp}, User: {user}'
        output = output.format(channel=self.channel or '',
                               text=self.text or '',
                               timestamp=self.timestamp or '',
                               user=self.user or '')
        return output
