from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Response, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from tortoise import Tortoise
import redis.asyncio as redis

from code.config import TORTOISE_CONFIG, settings
from code.handlers import webhook_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_conn = redis.from_url(str(settings.redis_url))
    await FastAPILimiter.init(redis_conn)
    await Tortoise.init(config=TORTOISE_CONFIG)

    yield

    await redis_conn.close()
    await FastAPILimiter.close()
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health/')
async def health():
    return Response(status_code=status.HTTP_200_OK)


app.add_api_route(
    '/webhook/',
    webhook_handler,
    methods=['POST'],
    dependencies=[Depends(RateLimiter(times=5, seconds=1))],
)


if __name__ == '__main__':
    uvicorn.run('code.app:app', host='0.0.0.0', port=8000, reload=True)
