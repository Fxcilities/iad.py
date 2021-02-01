from aiohttp import ClientSession, FormData


class Request:
    def __init__(self, http: ClientSession, route: str, method: str, headers: dict = None, data: dict = None, files: dict = None):
        self.route = 'https://im-a-dev.xyz/'
        self.route += route
        
        self.method = method
        self.headers = headers

        if data is not None:
            self.data = FormData()
            for k, v in data.items():
                self.data.add_field(k, v)

            if files is not None:
                for k, v in files.items():
                    self.data.add_field(k, v[1], filename=f'file.{v[0]}') # upload with correct file extension

        self.http = http
        
    async def json(self):
        if self.method == 'GET':
            async with self.http.get(self.route, headers=self.headers) as r:
                return await r.json()
        elif self.method == 'POST':
            async with self.http.post(self.route, headers=self.headers, data=self.data) as r:
                return await r.json()

    async def read(self):
        if self.method == 'GET':
            async with self.http.get(self.route, headers=self.headers) as r:
                return await r.read()
        elif self.method == 'POST':
            async with self.http.post(self.route, headers=self.headers, data=self.data) as r:
                return await r.read()
