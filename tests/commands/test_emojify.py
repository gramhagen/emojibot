# -*- coding: utf-8 -*-

from emojibot.commands.emojify import Emojify


def test_emojify():
    config = dict()

    test = Emojify(config=config)
    assert test.run(None) is None
