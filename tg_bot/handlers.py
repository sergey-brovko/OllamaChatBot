import asyncio
import logging

import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command

SERVER_URL = 'http://fastapi:8000'

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Hi, {message.from_user.full_name}")


@router.message(Command("info"))
async def cmd_info(message: Message):
    await message.answer(text="Help!")





@router.message(F.text)
async def reply_text(message: Message):
    request_id=''
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{SERVER_URL}/generate", json={"prompt": message.text}) as response:
            res = await response.json()
            request_id = res["request_id"]
    msg = await message.answer("⏳ Ваше сообщение обрабатывается...")
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(f"{SERVER_URL}/result/{request_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    await msg.edit_text(data['result'])
                    return
                await asyncio.sleep(2)




