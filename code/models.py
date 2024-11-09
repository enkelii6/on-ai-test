from tortoise import Model, fields

from code.types import RoleEnum


class MessageHistory(Model):
    id = fields.UUIDField(pk=True)
    user_id = fields.BigIntField(index=True)
    message = fields.TextField(max_length=4096)
    role = fields.CharEnumField(RoleEnum)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "message_history"
