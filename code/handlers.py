from fastapi import Depends, Response, status
from loguru import logger

from code.dependencies import get_user_id
from code.models import MessageHistory
from code.schemas import WebhookSchema
from code.celery import app, task
from code.types import RoleEnum


async def webhook_handler(data: WebhookSchema, user_id: int = Depends(get_user_id)):
    await MessageHistory.create(
        user_id=user_id,
        message=data.message,
        role=RoleEnum.USER,
    )

    async with app.setup():
        await task.delay(str(data.callback_url), user_id)
        logger.info('Message sent', user_id=user_id, message=data.message, callback_url=data.callback_url)

    return Response(status_code=status.HTTP_200_OK)
