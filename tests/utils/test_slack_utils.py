# -*- coding: utf-8 -*-

import os
import pytest

from tempfile import NamedTemporaryFile

from utils.slack_utils import connect, get_reference_token, get_messages, upload_file, send_response
from utils.reaction import Response


bot_name = 'a'
bot_id = 1
token = 'token'
command = 'command'
args = 'arg1 arg2'
prefix = 'nbot_slack_utils'
suffix = '.test'
link = 'link'
text = '1'
channel = 2
timestamp = 3
color = '4'
powt_kwargs = dict(attachments=[dict(mrkdwn_in=['fields'],
                                     color=color,
                                     fallback=text,
                                     fields=[dict(value=text, short=False)],
                                     image_url=None,
                                     ts=timestamp)],
                   as_user=True,
                   channel=channel)


@pytest.fixture
def client():

    # mock slack client
    class FakeClient(object):
        def set_retries(self, retries_needed):
            self.runs = 0
            self.retries_needed = retries_needed

        def rtm_connect(self):
            result = False if self.runs < self.retries_needed else True
            self.runs += 1
            return result

        def rtm_read(self):
            return [dict(text='{token}: {command} {args}'.format(token=token, command=command, args=args)), dict(), []]

        def api_call(self, method, **kwargs):
            if method == 'users.list':
                return dict(members=[dict(name=bot_name, id=bot_id), dict(name='b', id=2)])
            elif method == 'files.upload':
                assert kwargs['channel'] == channel
                assert kwargs['filename'].startswith(prefix) and kwargs['filename'].endswith(suffix)
                assert kwargs['title'].startswith(prefix)
                return dict(file=dict(permalink=link))
            elif method == 'chat.postMessage':
                assert kwargs == powt_kwargs
            else:
                raise KeyError('invalid method: %s', method)

    return FakeClient()


def test_connect(client):

    # no-retry
    client.set_retries(0)
    connect(client=client, attempts=2, base=0)
    assert client.runs == 1

    # with retry
    client.set_retries(1)
    connect(client=client, attempts=2, base=0)
    assert client.runs == 2

    # with failure
    client.set_retries(1)
    with pytest.raises(SystemError):
        connect(client=client, attempts=0)


def test_get_reference_token(client):

    assert get_reference_token(client=client, name=bot_name) == '<@{}>'.format(bot_id)

    with pytest.raises(KeyError):
        get_reference_token(client=client, name='invalid_bot_name')


def test_get_messages(client):

    messages = [m for m in get_messages(client=client, token=token)]
    assert len(messages) == 1
    assert str(messages[0]) == 'Args: {args}, Channel: , Command: {command}, User: '.format(args=args, command=command)


def test_upload_file(client):

    tmp_filename = NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False).name
    response = Response(filename=tmp_filename, channel=channel)

    assert os.path.isfile(tmp_filename)
    response = upload_file(client=client, response=response, delete=True)
    assert not os.path.isfile(tmp_filename)

    assert response.filename == link


def test_send_response(client):

    response = Response(text=text, channel=channel, timestamp=timestamp)
    send_response(client=client, response=response, color=color)
