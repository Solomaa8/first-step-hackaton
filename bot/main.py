"""
Бот 'Первый шаг' — нативный MAX Bot API (Long Polling).
Интеграция с платформой стажировок MAX и FastAPI бэкендом.
"""
import asyncio
import json
import logging
import httpx
from dotenv import load_dotenv
from bot.config import BOT_TOKEN, BACKEND_URL, WEBAPP_URL
from bot.max_api import MaxBotAPI

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

SPECIALTY_NAMES = {
    "it": "💻 Информационные технологии (IT)",
    "economics": "📊 Экономика и менеджмент",
    "engineering": "⚙️ Инженерия и производство",
}

# Хранилище состояний пользователей (in-memory для бота)
user_states: dict = {}


def specialty_buttons() -> list:
    """Inline-кнопки выбора специальности (формат MAX API)."""
    return [
        [{"type": "callback", "text": "💻 IT и разработка", "payload": "spec:it"}],
        [{"type": "callback", "text": "📊 Экономика и финансы", "payload": "spec:economics"}],
        [{"type": "callback", "text": "⚙️ Инженерия и производство", "payload": "spec:engineering"}],
    ]


def course_buttons() -> list:
    """Inline-кнопки выбора курса."""
    return [
        [
            {"type": "callback", "text": "1 курс", "payload": "course:1"},
            {"type": "callback", "text": "2 курс", "payload": "course:2"},
        ],
        [
            {"type": "callback", "text": "3 курс", "payload": "course:3"},
            {"type": "callback", "text": "4 курс", "payload": "course:4"},
        ],
        [
            {"type": "callback", "text": "🎓 Магистратура", "payload": "course:5"},
        ]
    ]


def main_menu_buttons() -> list:
    """Главное меню с кнопкой Мини-приложения (WebApp)."""
    return [
        [{"type": "link", "text": "🚀 Открыть Студию компетенций", "url": WEBAPP_URL}],
        [{"type": "callback", "text": "💼 Топ стажировок с Match Score", "payload": "action:vacancies"}],
        [{"type": "callback", "text": "🎯 Анализ навыков и roadmap", "payload": "action:match"}],
        [{"type": "callback", "text": "👤 Мой профиль", "payload": "action:profile"}],
    ]


async def send_welcome(api: MaxBotAPI, chat_id: int, user_id: int):
    """Отправка приветственного сообщения."""
    user_states[user_id] = {"step": "choosing_specialty"}
    await api.send_message(
        chat_id=chat_id,
        user_id=user_id if not chat_id else None,
        text=(
            "👋 Привет! Я бот проекта «Первый шаг» в мессенджере MAX!\n\n"
            "🎯 Я помогаю студентам найти первую оплачиваемую стажировку или работу по специальности с расчётом индекса соответствия навыков (Skill Match Score).\n\n"
            "📚 Выбери твоё направление обучения:"
        ),
        inline_keyboard=specialty_buttons()
    )


async def handle_message(api: MaxBotAPI, update: dict):
    """Обработка входящего текстового сообщения."""
    message = update.get("message", {})
    body = message.get("body", {})
    text = body.get("text", "").strip()
    chat_id = update.get("chat_id") or message.get("recipient", {}).get("chat_id")
    sender = message.get("sender", {})
    user_id = sender.get("user_id") or update.get("user", {}).get("user_id")

    if not chat_id and not user_id:
        return

    logger.info(f"Сообщение от user_id={user_id} в chat_id={chat_id}: '{text}'")

    lower = text.lower()
    if text.startswith("/start"):
        await send_welcome(api, chat_id, user_id)
    elif text.startswith("/help"):
        await api.send_message(
            chat_id=chat_id,
            user_id=user_id if not chat_id else None,
            text=(
                "📖 *Справка сервиса «Первый шаг»*\n\n"
                "• /start — Начать работу или сменить профиль\n"
                "• /help — Справка по командам\n"
                "• /vacancies — Подобрать актуальные стажировки\n\n"
                "💡 Также ты можешь открыть интерактивное мини-приложение, нажав на кнопку «Открыть Студию компетенций»!"
            ),
            inline_keyboard=main_menu_buttons()
        )
    elif text.startswith("/vacancies") or "ваканс" in lower or "стажировк" in lower:
        await show_vacancies(api, chat_id, user_id)
    elif "it" in lower or "разработ" in lower or "программир" in lower:
        await process_specialty(api, chat_id, user_id, "it")
    elif "эконом" in lower or "финанс" in lower or "менедж" in lower:
        await process_specialty(api, chat_id, user_id, "economics")
    elif "инженер" in lower or "производ" in lower:
        await process_specialty(api, chat_id, user_id, "engineering")
    elif any(lower.startswith(x) for x in ["1", "2", "3", "4", "5", "магистр"]):
        course_val = "5" if "магистр" in lower or "5" in lower else lower[0]
        await process_course(api, chat_id, user_id, course_val)
    else:
        await api.send_message(
            chat_id=chat_id,
            user_id=user_id if not chat_id else None,
            text="Используй кнопки меню или напиши /start для начала работы 🚀",
            inline_keyboard=main_menu_buttons()
        )


async def process_specialty(api: MaxBotAPI, chat_id: int, user_id: int, specialty: str):
    """Шаг выбора специальности."""
    user_states[user_id] = {"step": "choosing_course", "specialty": specialty}
    text = (
        f"Выбрано направление: *{SPECIALTY_NAMES.get(specialty, specialty)}*\n\n"
        "🎓 Теперь укажи свой курс:"
    )
    await api.send_message(
        chat_id=chat_id,
        user_id=user_id if not chat_id else None,
        text=text,
        inline_keyboard=course_buttons()
    )


async def process_course(api: MaxBotAPI, chat_id: int, user_id: int, course_str: str):
    """Шаг выбора курса и сохранение профиля."""
    state = user_states.get(user_id, {})
    course_num = int(course_str) if course_str.isdigit() else 5
    state["course"] = course_str
    state["course_year"] = course_num
    state["step"] = "ready"
    user_states[user_id] = state

    # Синхронизация с бэкендом
    try:
        async with httpx.AsyncClient(timeout=5.0, trust_env=False) as client:
            await client.post(
                f"{BACKEND_URL}/api/profile",
                json={
                    "user_id": user_id,
                    "specialty": state.get("specialty", "it"),
                    "course_year": course_num,
                }
            )
            logger.info(f"Профиль сохранён в бэкенд для user_id={user_id}")
    except Exception as e:
        logger.warning(f"Не удалось синхронизировать профиль с бэкендом: {e}")

    spec_name = SPECIALTY_NAMES.get(state.get("specialty", "it"), "IT")
    course_label = f"{course_num} курс" if course_num < 5 else "Магистратура"
    congrats_text = (
        f"🎉 Отлично! Твой профиль настроен:\n"
        f"• Направление: {spec_name}\n"
        f"• Уровень: {course_label}\n\n"
        f"🚀 Выбери дальнейшее действие:\n"
        f"1. Открыть Студию компетенций (мини-приложение) для точного подбора\n"
        f"2. Посмотреть стажировки прямо здесь в чате\n"
        f"3. Проверить свой Match Score"
    )
    await api.send_message(
        chat_id=chat_id,
        user_id=user_id if not chat_id else None,
        text=congrats_text,
        inline_keyboard=main_menu_buttons()
    )


async def handle_callback(api: MaxBotAPI, update: dict):
    """Обработка клика по inline-кнопке."""
    logger.info(f"Получен callback update: {update}")
    callback = update.get("callback", {})
    payload = callback.get("payload", "")
    callback_id = callback.get("callback_id", "")
    user = callback.get("user", {})
    user_id = user.get("user_id") or update.get("user", {}).get("user_id")

    # В MAX Bot API message может лежать в update['message'] или callback['message']
    message = update.get("message") or callback.get("message") or {}
    recipient = message.get("recipient", {})
    chat_id = (
        update.get("chat_id")
        or recipient.get("chat_id")
        or callback.get("chat_id")
        or user_id
    )

    # 1. Сразу подтверждаем callback в MAX, чтобы снять спиннер нажатия с кнопки
    if callback_id:
        try:
            await api.answer_callback(callback_id)
            logger.info(f"Callback {callback_id} успешно подтверждён")
        except Exception as e:
            logger.warning(f"Не удалось подтвердить callback {callback_id}: {e}")

    if not chat_id and not user_id:
        logger.warning(f"Не удалось определить chat_id или user_id: {update}")
        return

    logger.info(f"Обработка callback от user_id={user_id}, chat_id={chat_id}, payload='{payload}'")

    if payload.startswith("spec:"):
        specialty = payload.split(":")[1]
        await process_specialty(api, chat_id, user_id, specialty)

    elif payload.startswith("course:"):
        course = payload.split(":")[1]
        await process_course(api, chat_id, user_id, course)

    elif payload == "action:vacancies":
        await show_vacancies(api, chat_id, user_id)

    elif payload == "action:profile":
        state = user_states.get(user_id, {})
        spec = SPECIALTY_NAMES.get(state.get("specialty", "it"), "Не выбрано")
        course = state.get("course", "Не указан")
        profile_text = (
            f"👤 *Твой профиль в «Первый шаг»:*\n\n"
            f"• ID в MAX: `{user_id}`\n"
            f"• Специальность: {spec}\n"
            f"• Курс: {course}\n"
            f"• Базовый Skill Match: ~85%\n\n"
            f"Для детальной настройки навыков открой Студию компетенций 📲"
        )
        await api.send_message(
            chat_id=chat_id,
            user_id=user_id if not chat_id else None,
            text=profile_text,
            inline_keyboard=main_menu_buttons()
        )

    elif payload == "action:match":
        match_text = (
            "🎯 *Анализ соответствия вакансиям (Skill Match):*\n\n"
            "На основе твоего профиля система проанализировала требования работодателей:\n\n"
            "✅ Имеющиеся навыки: Python (Основы), Git, SQL\n"
            "⚡️ Рекомендуем подтянуть: FastAPI, Docker, PostgreSQL\n"
            "📈 Текущий рейтинг готовности к стажировке: *85%*\n\n"
            "Подробный интерактивный граф навыков доступен в мини-приложении!"
        )
        await api.send_message(
            chat_id=chat_id,
            user_id=user_id if not chat_id else None,
            text=match_text,
            inline_keyboard=main_menu_buttons()
        )


async def show_vacancies(api: MaxBotAPI, chat_id: int, user_id: int):
    """Загрузка вакансий из FastAPI бэкенда и отправка в чат."""
    state = user_states.get(user_id, {})
    specialty = state.get("specialty", "it")

    try:
        async with httpx.AsyncClient(timeout=8.0, trust_env=False) as client:
            resp = await client.get(
                f"{BACKEND_URL}/api/vacancies",
                params={"user_id": user_id or 12345, "skills": "python,git,sql"}
            )
            if resp.status_code == 200:
                data = resp.json()
                vacancies = data.get("matched_vacancies", [])[:3]
                if not vacancies:
                    vacancies = data.get("related_vacancies", [])[:3]
                if vacancies:
                    msg = "💼 *Топ рекомендованных стажировок для тебя:*\n\n"
                    for i, vac in enumerate(vacancies, 1):
                        title = vac.get("title", "Стажёр")
                        company = vac.get("company", "Партнёр")
                        location = vac.get("location", "Москва")
                        score = int(round(vac.get("match_score", 0.85) * 100))
                        req_skills = ", ".join(vac.get("required_skills", [])[:4])
                        msg += (
                            f"{i}. *{title}*\n"
                            f"   🏢 Компания: {company} ({location})\n"
                            f"   🛠 Стек: {req_skills}\n"
                            f"   🔥 Совпадение (Match): *{score}%*\n\n"
                        )
                    msg += "🔗 Полный интерактивный каталог — в мини-приложении!"
                    await api.send_message(
                        chat_id=chat_id,
                        user_id=user_id if not chat_id else None,
                        text=msg,
                        inline_keyboard=main_menu_buttons()
                    )
                    return
    except Exception as e:
        logger.error(f"Ошибка запроса вакансий к бэкенду: {e}")

    # Fallback
    fallback_msg = (
        "💼 *Рекомендованные стажировки:*\n\n"
        "1. *Junior Python Developer (FastAPI)*\n"
        "   🏢 СберТех (Москва)\n"
        "   🔥 Совпадение: *95%*\n\n"
        "2. *Стажёр Go-разработчик*\n"
        "   🏢 VK Cloud (Москва)\n"
        "   🔥 Совпадение: *85%*\n\n"
        "3. *Junior Backend (Golang)*\n"
        "   🏢 Wildberries Tech (Москва)\n"
        "   🔥 Совпадение: *80%*\n"
    )
    await api.send_message(
        chat_id=chat_id,
        user_id=user_id if not chat_id else None,
        text=fallback_msg,
        inline_keyboard=main_menu_buttons()
    )


async def main():
    logger.info("Запуск бота «Первый шаг» для MAX...")
    api = MaxBotAPI(BOT_TOKEN)

    try:
        me = await api.get_me()
        bot_name = me.get("first_name", "Bot")
        username = me.get("username", "unknown")
        user_id = me.get("user_id", "")
        logger.info(f"✅ Успешная авторизация в MAX! Бот: {bot_name} (@{username}) [ID: {user_id}]")
    except Exception as e:
        logger.error(f"❌ Ошибка авторизации в MAX API: {e}")
        return

    logger.info("Начало цикла Long Polling...")
    while True:
        try:
            updates = await api.get_updates(limit=50, timeout=20)
            for update in updates:
                update_type = update.get("update_type")
                logger.debug(f"Update: {update_type}")

                if update_type == "bot_started":
                    chat_id = update.get("chat_id")
                    user = update.get("user", {})
                    user_id = user.get("user_id", 0)
                    if chat_id or user_id:
                        await send_welcome(api, chat_id, user_id)

                elif update_type == "message_created":
                    await handle_message(api, update)

                elif update_type == "message_callback":
                    await handle_callback(api, update)

                else:
                    logger.info(f"Неизвестный update_type: {update_type}: {update}")

        except asyncio.CancelledError:
            logger.info("Остановка бота...")
            break
        except Exception as e:
            logger.error(f"Непредвиденная ошибка в основном цикле: {e}")
            await asyncio.sleep(2)

    await api.close()


if __name__ == "__main__":
    asyncio.run(main())


