from datetime import datetime
from io import BytesIO
from os import path
from typing import Union

from aiohttp import ClientSession

from ..errors import InvalidContentType, JsonDecodeException, RequestError
from ..ratelimit import RateLimiter
from ..request import Request
from .upload import Upload


class ImADev:
    """
    Main class for iad.py
    """

    DISABLED = ('php', 'html', 'js', 'css', 'ts')
    def __init__(self, token, session = None):
        assert isinstance(token, str), f"token argument expected str, got {token.__class__.__name__}"
        
        self.__token = token
        self._http = RateLimiter(session or ClientSession())

    def __repr__(self):
        return f"<ImADev token={self.__token} http={self._http}>"

    async def upload(self, data, file_format: str = None) -> Upload:
        """
        Upload a file to im-a-dev.xyz

        :param data: either :class:`io.BytesIO` file buffer, :class:`bytes` file bytes, or `:class:`str` file path
        :param file_format: must be :class:`str`, can be ``None`` if data is str.
        :return: Returns a :class:`iad.model.Upload`
        """

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
            raise InvalidContentType(file_format)

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


    async def delete(self, filename: Union[Upload, str]) -> bool:
        """
        :param filename: must be either a :class:`iad.model.Upload` or a :class:`str` representing the file/filename
        :return: Returns a :class:`bool` if it was succsesful or not.
        """

        assert type(filename) in [Upload, str], f"filename expected str or upload, got {filename.__class__.__name__}"

        req = Request(self._http, 'upload.php', 'POST', data={
            'token': self.__token,
            'endpoint': 'delete',
            'filename': filename
        })

        try:
            json = await req.json()
        except:
            raise JsonDecodeException(await req.read())

        return (json['http_code'] == 200)

    async def get_upload(self, filename: str) -> Upload:
        """
        :param filename: Name of the file to get
        :return: Returns a :class:`iad.model.Upload` of the fetched upload.
        """
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
