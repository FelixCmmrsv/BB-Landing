from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import backend.app.database.requests as rq


async def main():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Все заявки', callback_data='requests'))
    return kb.adjust(2).as_markup()


async def requests(start=0, limit=8):
    kb = InlineKeyboardBuilder()
    users = await rq.get_users_not_agreed()
    for user in users[start:start + limit]:
        kb.add(InlineKeyboardButton(text=f'{user.first_name} {user.last_name}', callback_data=f'user_{user.id}'))
    if start + limit < len(users):
        kb.add(InlineKeyboardButton(text='Еще', callback_data=f'more_{start + limit}'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='back_main'))
    return kb.adjust(1).as_markup()


async def user_selected(user_id):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Добавить', callback_data=f'approve_{user_id}'))
    kb.add(InlineKeyboardButton(text='Отклонить', callback_data=f'reject_{user_id}'))
    kb.add(InlineKeyboardButton(text='Назад', callback_data='back_requests'))
    return kb.adjust(2).as_markup()

