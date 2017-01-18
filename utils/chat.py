# -*- coding: utf-8 -*-
"""Base Response object"""

from time import time

from emojibot.utils.response import Response


class Chat(Response):
    """Chat message class"""

    api_method = 'chat.postMessage'
    color = None
    text = None

    def __init__(self, channel, text, color='#2874A6'):
        """Constructor

        Args:
            channel (str): channel of chat message
            text (str): text of chat message
            color (str): optional, color of message bar
        """

        self.color = color
        self.text = text

        super(Chat, self).__init__(channel=channel)

    def to_dict(self):
        """Represent arguments for api call as a dict"""

        output = dict(as_user=True, channel=self.channel)
        entries = self.text if isinstance(self.text, list) else [self.text]
        fallback = '\n'.join(entries)
        fields = [dict(value=entry, short=False) for entry in entries]

        output['attachments'] = [dict(mrkdwn_in=['fields'],
                                      color=self.color,
                                      fallback=fallback,
                                      fields=fields,
                                      ts=time())]

        return output
