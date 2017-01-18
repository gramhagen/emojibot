# -*- coding: utf-8 -*-
"""Reaction Class Container"""

from emojibot.utils.response import Response


class Reaction(Response):
    """Reaction class"""

    api_method = 'reactions.add'
    channel = None
    name = None
    timestamp = None

    def __init__(self, channel, name, timestamp):
        """Constructor

        Args:
            channel (str): slack channel to send reaction to
            name (str): name of emoji
            timestamp (float): timestamp of message to add reaction to
        """

        self.name = name
        self.timestamp = timestamp

        super(Reaction, self).__init__(channel=channel)

    def to_dict(self):
        """Dictionary representation of class"""
        return dict(channel=self.channel, name=self.name, timestamp=self.timestamp)

    def __repr__(self):
        """String representation of class"""

        output = 'Channel: {channel}, Name: {name}, Timestamp: {timestamp}'
        output = output.format(channel=self.channel or '',
                               name=self.name or '',
                               timestamp=self.timestamp)
        return output
