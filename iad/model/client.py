import asyncio
from datetime import datetime
from io import BytesIO
from typing import Tuple

import PIL
from aiohttp import ClientSession

from ..errors import (InvalidContentType, InvalidToken, JsonDecodeException,
                      RequestError)
from ..ratelimit import RateLimiter
from ..request import Request
from .upload import Upload


class ImADev:

    DISABLED = ('php', 'html', 'js', 'css', 'ts')

    def __init__(self, token: str = None):

        self.token = token
        self._http = ClientSession()
        self._http = RateLimiter(self._http)

        if self.token is None:
            raise ValueError('No token specified')
        elif type(self.token) != str:
            raise ValueError('token argument not str, got {}'.format(self.token.__class__.__name__))

    async def upload(self, data: Tuple[str, bytes] = None):
        file = data[1]
        if data is None:
            raise ValueError('file argument not specified')
        if type(file) != bytes:
            raise ValueError('file argument not bytes, got {}'.format(file.__class__.__name__))

        if(data[0] in self.DISABLED):
            raise InvalidContentType('{} is a API blacklisted file extension.'.format(data[0]))
        
        payload = {
            'token': self.token,
            'endpoint': 'upload'
        }

        files = { "image": data }

        req = Request(self._http, 'upload.php', 'POST', data=payload, files=files)
        try:
            json = await req.json()
        except:
            raise JsonDecodeException('Failed to decode json from API. Raw content:\n\n' + str(await req.read()))
        try:
            return Upload(json['filename'], json['username'], json['url'].replace("\\", ""), datetime.now())
        except:
            if 'error' in json:
                raise RequestError(json['error'])
            else:
                raise RequestError('fatal error uploading.')

    async def get_upload(self, filename: str = None):
        if filename is None:
            raise ValueError('filename argument not specified')
        if type(filename) != str:
            raise ValueError('filename argument not str, got {}'.format(filename.__class__.__name__))

        payload = {
            'token': self.token,
            'endpoint': 'get_upload',
            'filename': filename
        }

        req = Request(self._http, 'upload.php', 'POST', data=payload)
        try:
            json = await req.json()
        except:
            raise JsonDecodeException('Failed to decode json from API. Raw content:\n\n' + await req.read())
        try:
            return Upload(json['filename'], json['username'], json['url'].replace("\\", ""), datetime.strptime(json['uploaded_at'], '%B %d %Y %H:%M:%S'))
        except:
            if 'error' in json:
                raise RequestError(json['error'])
            else:
                raise RequestError('fatal error getting upload info.')
