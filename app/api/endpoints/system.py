import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app import schemas
from app.core.config import settings
from app.core.security import verify_token
from app.helper.message import MessageHelper
from app.helper.progress import ProgressHelper

router = APIRouter()


@router.get("/progress/{process_type}", summary="实时进度")
async def get_progress(process_type: str, token: str):
    """
    实时获取处理进度，返回格式为SSE
    """
    if not token or not verify_token(token):
        raise HTTPException(
            status_code=403,
            detail="认证失败！",
        )

    progress = ProgressHelper()

    async def event_generator():
        while True:
            detail = progress.get(process_type)
            yield 'data: %s\n\n' % json.dumps(detail)
            await asyncio.sleep(0.2)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/message", summary="实时消息")
async def get_progress(token: str):
    """
    实时获取系统消息，返回格式为SSE
    """
    if not token or not verify_token(token):
        raise HTTPException(
            status_code=403,
            detail="认证失败！",
        )

    message = MessageHelper()

    async def event_generator():
        while True:
            detail = message.get()
            yield 'data: %s\n\n' % detail
            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
