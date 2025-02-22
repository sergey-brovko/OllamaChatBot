import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import router


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(token=os.getenv('TELEGRAM_BOT_KEY'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info('Bot started')
    except KeyboardInterrupt:
        logger.info('Bot stopped')
