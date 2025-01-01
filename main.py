import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from backend.app.handlers import router, bot
from backend.app.middlewares import CallbackAnswerMiddleware
from backend.app.database.models import async_main

from quart import Quart
from backend.site.registration import registration

load_dotenv()

app = Quart(__name__)
app.register_blueprint(registration, url_prefix="/registration")

async def start_telegram_bot():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Bot started")

    await async_main()

    dp = Dispatcher()
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.include_router(router)
    await dp.start_polling(bot)


async def start_flask_app():
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5000"]
    await serve(app, config)


async def main():
    await asyncio.gather(
        start_telegram_bot(),
        start_flask_app(),
    )


if __name__ == "__main__":
    asyncio.run(main())
