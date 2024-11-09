from fastapi import Request

async def get_user_id(request: Request):
    return request.headers.get('x-user-id')
