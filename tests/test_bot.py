# -*- coding: utf-8 -*-

import pytest
import slackclient

from emojibot import commands
from emojibot import memory

from emojibot.utils.message import Message
from emojibot.utils.response import Response
from emojibot.utils import slack_utils


class FakeClient(object):
    def __init__(self, api_token):
        assert api_token == api_token


class FakeCommand(object):
    def run(self, cmd):
        if cmd:
            return Response(text=cmd)
        else:
            raise Exception('barf')

fake_api_token = 1
fake_bot_name = 2
fake_read_delay = 3
fake_channel = 'channel'
fake_message = 'message'
fake_token = 'token'
fake_command_list = dict(a=FakeCommand())


@pytest.fixture()
def bot(monkeypatch):

    def fake_init_db(config):
        pass
    monkeypatch.setattr(memory, 'init_db', fake_init_db)

    def fake_log_action(command, success):
        pass
    monkeypatch.setattr(memory, 'log_action', fake_log_action)

    def fake_get_command_list(config):
        return fake_command_list
    monkeypatch.setattr(commands, 'get_command_list', fake_get_command_list)

    monkeypatch.setattr(slackclient, 'SlackClient', FakeClient)

    def fake_connect(client):
        assert isinstance(client, FakeClient)
    monkeypatch.setattr(slack_utils, 'connect', fake_connect)

    def fake_get_reference_token(client, name):
        assert isinstance(client, FakeClient)
        assert name == fake_bot_name
        return fake_token
    monkeypatch.setattr(slack_utils, 'get_reference_token', fake_get_reference_token)

    def fake_get_messages(client, token):
        assert isinstance(client, FakeClient)
        assert token == fake_api_token
        data = dict(text=fake_message, channel=fake_channel, user=fake_bot_name)
        return Message.from_dict(input_dict=data, token=token)
    monkeypatch.setattr(slack_utils, 'get_messages', fake_get_messages)

    from bot import Bot
    config = dict(LOG_CONFIG=dict(version=1))
    return Bot(api_token=fake_api_token, bot_name=fake_bot_name, config=config, read_delay=fake_read_delay)


def test_init(bot):
    assert bot.api_token == fake_api_token
    assert bot.bot_name == fake_bot_name
    assert bot.command_list == fake_command_list
    assert bot.read_delay == fake_read_delay


def test_process_message(bot):

    args = '1'

    # test valid message
    valid_message = Message(args=args, command='a', channel=fake_channel)
    response = bot.process_message(valid_message)
    assert response.channel == fake_channel
    assert response.text == args

    # test invalid command
    invalid_message = Message(command='b')
    response = bot.process_message(message=invalid_message)
    assert response.text == ['I did not understand that. Try: *help*\n']

    # test exception
    error_message = Message(command='a')
    response = bot.process_message(message=error_message)
    assert response.text == ['Sorry I could not process that.', 'barf']


def test_start(bot):
    # TODO: add test here
    pass
