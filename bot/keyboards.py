from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from bot.config import WEBAPP_URL


def specialty_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💻 Информационные технологии", callback_data="spec:it")],
        [InlineKeyboardButton(text="📊 Экономика и управление", callback_data="spec:economics")],
        [InlineKeyboardButton(text="⚙️ Инженерия и производство", callback_data="spec:engineering")],
    ])


def course_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 курс", callback_data="course:1"),
            InlineKeyboardButton(text="2 курс", callback_data="course:2"),
        ]
    ])


def main_menu_keyboard(webapp_url: str = WEBAPP_URL) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🚀 Пройти аудит компетенций",
                web_app=WebAppInfo(url=webapp_url)
            )],
            [KeyboardButton(text="👤 Мой профиль")],
            [KeyboardButton(text="🔔 Обновить вакансии")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back:start")]
    ])
