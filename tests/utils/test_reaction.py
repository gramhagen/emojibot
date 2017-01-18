# -*- coding: utf-8 -*-

from emojibot.utils.response import Response


def test_constructor():
    response = Response()
    assert isinstance(response, Response)
