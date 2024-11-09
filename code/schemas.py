from pydantic import BaseModel
from pydantic_core import Url


class WebhookSchema(BaseModel):
    message: str
    callback_url: Url
