# -*- coding: utf-8 -*-
# pylint: disable=unused-import
"""Container for Slack utilities

   Reference: http://slackapi.github.io/python-slackclient/
"""

import logging
import time

from slackclient import SlackClient

from emojibot.utils.message import Message


def connect(client, attempts=5, base=2):
    """Connect to client with exponential backoff on re-attempts

    Args:
        client (SlackClient): slack client
        attempts (int): number of attempts to try
        base (int): base number to raise to growing power

    Returns:
        (boolean): result of connection attampts
    """

    for attempt in range(attempts):
        if client.rtm_connect():
            return True
        time.sleep(base ** (attempt + 1))

    raise SystemError('Could not connect to Slack')


def get_reference_token(client, name):
    """Get slack reference token given name

    Args:
        client (SlackClient): slack client
        name (str): member name to search for

    Returns:
        (str): slack reference token
    """

    for member in client.api_call('users.list')['members']:
        if member['name'] == name:
            return '<@{0[id]}>'.format(member)

    raise KeyError('Could not find user with name: %s', name)


def get_messages(client, bot_ref):
    """Generator to get relevant messages from slack

    Args:
        client (SlackClient): slack client
        bot_ref (str): bot reference to use for filtering relevant messages

    Returns:
        (generator<Message>): relevant messages
    """

    try:
        messages = client.rtm_read()
    except Exception as e:
        logging.error('Error connecting to slack: %s', e, exc_info=True)
        # connection dropped, reconnect
        connect(client=client)
        messages = []

    for message in messages:
        try:
            if (message.get('text') or '').startswith(bot_ref):
                relevant_message = Message(bot_ref=bot_ref, **message)
                logging.debug('Received message: %s', relevant_message)
                yield relevant_message
        except Exception as e:
            logging.error('Error constructing message: %s', e, exc_info=True)
