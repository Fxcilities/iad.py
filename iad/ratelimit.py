import asyncio
import time

from aiohttp import ClientSession

"""
Idea: https://quentin.pradet.me/blog/how-do-you-rate-limit-calls-with-aiohttp.html
"""


class RateLimiter:
    RATE = 16 # 16 per second
    TOKENS = 16
    
    def __init__(self, session):
        self.client = session
        self.tokens = self.TOKENS
        self.updated_at = time.monotonic()

    async def get(self, *args, **kwargs): # GET override
        await self.wait_for_token()
        return self.client.get(*args, **kwargs)

    async def post(self, *args, **kwargs): # POST override
        await self.wait_for_token()
        return self.client.post(*args, **kwargs)

    async def wait_for_token(self):
        while self.tokens <= 1:
            await self.add_token()
            await asyncio.sleep(1)
        self.tokens -= 1

    def add_token(self):
        now = time.monotonic()
        since_updated = now - self.updated_at
        new_tokens = since_updated * self.RATE
        if self.tokens + new_tokens >= 1:
            self.tokens = min(self.tokens + new_tokens, self.TOKENS)
            self.updated_at = now
