import asyncio
from aiohttp import ClientSession
from ..request import Request
import PIL
from io import BytesIO
from typing import Tuple
from .upload import Upload
from ..errors import RequestError


class ImADev:
    def __init__(self, token: str = None):

        self.token = token
        self._http = ClientSession()
        self._ratelimits = {
            "upload": None,
            "get_upload": None
        }

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

        
        payload = {
            'token': self.token,
            'endpoint': 'upload'
        }

        files = { "image": data }

        req = Request(self._http, 'upload.php', 'POST', data=payload, files=files)
        json = await req.json()

        try:
            return Upload(json['filename'], json['username'], json['url'].replace("\\", ""))
        except:
            raise RequestError(json['error'])

    async def get_upload(self, filename: str = None):
        if filename is None:
            raise ValueError('filename argument not specified')
        if type(filename) != str:
            raise ValueError('filename argument not str, got {}'.format(filename.__class__.__name__))

        payload = {
            'token': self.token,
            'endpoint': 'get_upload'
        }

        req = Request(self._http, 'upload.php', 'POST', data=payload)
        return await req.read()