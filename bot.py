# -*- coding: utf-8 -*-
# pylint: disable=too-many-arguments,no-value-for-parameter,redefined-variable-type
"""Main Bot module"""

import logging
import logging.config
import time

import click
import yaml

from slackclient import SlackClient

from emojibot.commands.emojify import Emojify
from emojibot.utils.chat import Chat
from emojibot.utils.slack_utils import connect, get_messages, get_reference_token


class Bot(object):
    """Bot Class"""

    api_token = None
    bot_name = None
    command_list = None
    read_delay = None

    def __init__(self, api_token, bot_name, config, read_delay=1):

        # setup logging
        try:
            logging.config.dictConfig(config['LOG_CONFIG'])
        except Exception as e:
            logging.error('Could not configure logging: %s', e, exc_info=True)

        logging.info('Starting: %s', bot_name)

        # instantiate emojify command
        self.emojify = Emojify(config=config)

        self.api_token = api_token
        self.bot_name = bot_name
        self.read_delay = read_delay

    def process_message(self, message):
        """Return results from executing a user command

        Args:
            message (Message): message to process
        Returns:
            (Response): processed response
        """

        try:
            logging.debug('Processing command: %s', message.text)
            response = self.emojify.run(channel=message.channel, text=message.text, timestamp=message.timestamp)
        except Exception as e:
            logging.error('Error processing text: %s. %s', message.text, e, exc_info=True)
            response = Chat(channel=message.channel, text=['Sorry I could not process that.', str(e)])

        return response

    def start(self):
        """Start Bot"""

        # setup slack client
        logging.debug('Connecting to slack...')
        slack_client = SlackClient(self.api_token)
        logging.debug('Connected to slack client')

        # connect slack client
        if not connect(client=slack_client):
            raise NameError('Connection failed. Invalid Slack API Token?')

        bot_ref = get_reference_token(client=slack_client, name=self.bot_name)
        logging.debug('Listening for messages starting with: %s', bot_ref)

        logging.debug('Starting message processing loop')
        while True:
            start = time.time()

            for message in get_messages(client=slack_client, bot_ref=bot_ref):
                response = self.process_message(message=message)
                response.send(client=slack_client)

            remaining = self.read_delay - (time.time() - start)
            if remaining > 0:
                time.sleep(remaining)


@click.command(context_settings=dict(help_option_names=['-?', '-h', '--help']))
@click.argument('config_file', type=click.File('rb'))
@click.option('--slack_api_token', type=str)
@click.option('--bot_name', type=str)
@click.option('--read_delay', type=int)
def start_bot(config_file, slack_api_token, bot_name, read_delay):
    """Start Bot

    Args:
        config_file (str): path to config file
        slack_api_token (str): Slack API token, if not provided will be looked up from config
        bot_name (str): bot name to listen for
        read_delay (int): seconds between slack rtm pulls
    """

    # load configuration from file
    config = yaml.load(config_file)

    slack_api_token = slack_api_token or config['SLACK_API_TOKEN']
    bot_name = bot_name or config.get('BOT_NAME', 'emojibot')
    read_delay = read_delay or config.get('SLACK_READ_DELAY', 1)

    Bot(api_token=slack_api_token, bot_name=bot_name, config=config, read_delay=read_delay).start()

if __name__ == '__main__':
    start_bot()
