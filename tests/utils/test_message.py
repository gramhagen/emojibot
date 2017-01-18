# -*- coding: utf-8 -*-

from utils.message import Message


def test_constructor():
    message = Message(args='1', channel='2', command='3', user='4')
    assert isinstance(message, Message)
    assert message.args == '1'
    assert message.channel == '2'
    assert message.command == '3'
    assert message.user == '4'


def test_repr():
    message = Message(args='1', channel='2', command='3', user='4')
    assert str(message) == 'Args: 1, Channel: 2, Command: 3, User: 4'


def test_from_dict():
    input_dict = dict(text='5: 3 1', channel='2', user='4')
    message = Message.from_dict(input_dict=input_dict, token='5')
    assert message.args == '1'
    assert message.channel == '2'
    assert message.command == '3'
    assert message.user == '4'
