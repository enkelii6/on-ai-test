from contextlib import asynccontextmanager

from aiohttp import ClientSession


@asynccontextmanager
async def create_http_client():
    async with ClientSession() as session:
        yield session
