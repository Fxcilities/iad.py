import time
from aiohttp import ClientSession
from asyncio import sleep

"""
Idea: https://quentin.pradet.me/blog/how-do-you-rate-limit-calls-with-aiohttp.html
"""

class RateLimiter:
    TOKENS = 16
    
    def __init__(self, session):
        assert isinstance(session, ClientSession), f"Invalid type for session argument, got {session.__class__.__name__}"
        self.client = session
        self.tokens = self.TOKENS
        self.updated_at = time.monotonic()

    async def get(self, *args, **kwargs): # GET override
        await self.wait_for_token()
        return await self.client.get(*args, **kwargs)

    async def post(self, *args, **kwargs): # POST override
        await self.wait_for_token()
        return await self.client.post(*args, **kwargs)

    async def wait_for_token(self):
        while self.tokens <= 1:
            self.add_token()
            await sleep(1)
        self.tokens -= 1

    def add_token(self):
        now = time.monotonic()
        since_updated = now - self.updated_at
        new_tokens = since_updated * 16
        if (self.tokens + new_tokens) >= 1:
            self.tokens = min(self.tokens + new_tokens, self.TOKENS)
            self.updated_at = now