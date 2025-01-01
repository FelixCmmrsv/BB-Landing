import os

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from dotenv import load_dotenv

import backend.app.keyboards as kb
import backend.app.database.requests as rq

bot = Bot(token=os.getenv("TG_API_TOKEN"))

router = Router()

load_dotenv()

@router.message(CommandStart())
async def start(message: Message):
    if message.from_user.id == 1181031286:
        await message.answer("Hello! I'm a bot!", reply_markup=await kb.main())

# Notify Func
async def notify_new_user(new_user):
    try:
        await bot.send_message(
            1181031286,
            f"New user registered:\n{new_user.first_name} {new_user.last_name}"
        )
    except Exception as e:
        print(f"Error notifying about new user: {e}")

# Request Func
@router.callback_query(F.data == 'requests')
async def process_requests_callback(callback_query: CallbackQuery, bot: Bot):
    await callback_query.message.edit_text("List of requests:", reply_markup=await kb.requests())


@router.callback_query(F.data.startswith('user_'))
async def process_user_selected_callback(callback_query: CallbackQuery):
    user_id = int(callback_query.data.split('_')[1])
    user = await rq.get_user_by_id(user_id)
    await callback_query.message.edit_text(f"User selected with ID: {user_id}"
                                           f"\nFirst name: {user.first_name}"
                                           f"\nLast name: {user.last_name}"
                                           f"\nUsername: {user.username}"
                                           f"\nEmail: {user.email}"
                                           f"\nProfile: {user.profile}"
                                           f"\nComments: {user.description}"
                                           f"\nCreated: {user.created_at}"
                                           f"\nWhat do you want to do with this user?",
                                           reply_markup=await kb.user_selected(user_id))


@router.callback_query(F.data.startswith('approve_'))
async def process_approve_callback(callback_query: CallbackQuery):
    user_id = int(callback_query.data.split('_')[1])
    await rq.approve_user(user_id)
    await callback_query.message.edit_text("User approved!", reply_markup=await kb.requests())


@router.callback_query(F.data.startswith('reject_'))
async def process_reject_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Dannaya function eshe ne dovedena do uma", reply_markup=await kb.requests())


@router.callback_query(F.data and F.data.startswith('more_'))
async def process_more_callback(callback_query: CallbackQuery):
    start_index = int(callback_query.data.split('_')[1])
    await callback_query.message.edit_reply_markup(reply_markup=await kb.requests(start=start_index))

# Back Func
@router.callback_query(F.data == 'back_requests')
async def process_back_requests_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text("List of requests:", reply_markup=await kb.requests())


@router.callback_query(F.data == 'back_main')
async def process_back_main_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Hello! I'm a bot!", reply_markup=await kb.main())