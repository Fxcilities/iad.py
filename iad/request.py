from aiohttp import FormData
from .ratelimit import RateLimiter

class Request:
    def __init__(self, http: RateLimiter, route: str, method: str, headers: dict = {}, data: dict = {}, files: dict = {}):
        self.route = f'https://im-a-dev.xyz/{route or ""}'
        self.method = method
        self.headers = headers
        self.http = http

        if data:
            self.data = FormData()
            for k, v in data.items():
                self.data.add_field(k, v)

            if files:
                self.data.add_field("image", files['bytes'], filename=f'file.{files["format"]}') # upload with correct file extension
        
    async def json(self):
        if self.method == 'GET':
            async with await self.http.get(self.route, headers=self.headers) as r:
                return await r.json()
        elif self.method == 'POST':
            async with await self.http.post(self.route, headers=self.headers, data=self.data) as r:
                return await r.json()

    async def read(self):
        if self.method == 'GET':
            async with await self.http.get(self.route, headers=self.headers) as r:
                return await r.read()
        elif self.method == 'POST':
            async with await self.http.post(self.route, headers=self.headers, data=self.data) as r:
                return await r.read()
