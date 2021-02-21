from datetime import datetime
from io import BytesIO
from aiohttp import ClientSession
from os import path
from ..errors import JsonDecodeException, RequestError
from ..ratelimit import RateLimiter
from ..request import Request
from .upload import Upload

class ImADev:
    DISABLED = ('php', 'html', 'js', 'css', 'ts')
    def __init__(self, token, session = None):
        assert isinstance(token, str), f"token argument expected str, got {token.__class__.__name__}"
        self.__token = token
        self._http = RateLimiter(session or ClientSession())

    def __repr__(self):
        return f"<ImADev token={token}>"

    async def upload(self, data, file_format: str = None):
        if isinstance(data, str):
            assert isinstance(data, str), "file_format argument not specified"
            assert path.isfile(data), f"File not found: {data}"
            if (not file_format) or (not isinstance(file_format, str)): # if file format is not specified, we try to find it from the path
                file_format = data.strip("\\").strip("/").split(".")[-1]
            data = open(data, "rb").read()
        elif isinstance(data, BytesIO):
            data = data.getvalue()
        else:
            assert isinstance(data, bytes), f"data argument type excepted bytes, got {data.__class__.__name__}"
        
        assert bool(file_format), "file_format argument not specified"

        if file_format.lower() in self.DISABLED:
            raise InvalidContentType(f'{file_format} is an API blacklisted file extension.')

        req = Request(self._http, 'upload.php', 'POST', data={
            'token': self.__token,
            'endpoint': 'upload'
        }, files={ "bytes": data, "format": file_format })
        try:
            json = await req.json()
        except:
            raise JsonDecodeException(await req.read())
        try:
            return Upload(json)
        except:
            raise RequestError(json)

    async def get_upload(self, filename: str):
        if not isinstance(filename, str):
            raise TypeError(f'filename argument expected str, got {filename.__class__.__name__}')

        req = Request(self._http, 'upload.php', 'POST', data={
            'token': self.__token,
            'endpoint': 'get_upload',
            'filename': filename
        })
        try:
            json = await req.json()
        except:
            raise JsonDecodeException(await req.read())
        try:
            return Upload(json, time=datetime.strptime(json['uploaded_at'], '%B %d %Y %H:%M:%S'))
        except:
            raise RequestError(json)
