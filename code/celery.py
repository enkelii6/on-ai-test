from contextlib import asynccontextmanager

from loguru import logger
from tortoise import Tortoise
from aio_celery import Celery

from code.config import TORTOISE_CONFIG, settings
from code.models import MessageHistory
from code.clients.open_ai import client as openai_client
from code.clients.http import create_http_client
from code.types import RoleEnum


app = Celery()
app.conf.broker_url = str(settings.rabbit_mq_url)


@app.task
async def task(callback_url: str, user_id: int):
    message_history = await MessageHistory.filter(user_id=user_id).order_by('created_at').all()

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    'role': message.role,
                    'content': message.message,
                } for message in message_history
            ]
        )
    except Exception as e:
        logger.error('Trouble while getting response from chatgpt', e)

    async with create_http_client() as http_client:
        await http_client.post(str(callback_url), {'message': completion.choices[0].message.content})

    await MessageHistory.create(
        user_id=user_id,
        message=completion.choices[0].message.content,
        role=RoleEnum.SYSTEM,
    )


@app.define_app_context
@asynccontextmanager
async def startup():
    await Tortoise.init(config=TORTOISE_CONFIG)
    logger.info('Starting app...')

    try:
        yield
    finally:
        await Tortoise.close_connections()
