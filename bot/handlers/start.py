import httpx
import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards import specialty_keyboard, course_keyboard, main_menu_keyboard
from bot.config import BACKEND_URL

router = Router()

SPECIALTY_NAMES = {
    "it": "💻 Информационные технологии",
    "economics": "📊 Экономика и управление",
    "engineering": "⚙️ Инженерия и производство",
}

COURSE_NAMES = {1: "1 курс", 2: "2 курс"}


class Registration(StatesGroup):
    choosing_specialty = State()
    choosing_course = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Я — *Первый шаг*, твой карьерный навигатор.\n\n"
        "Помогу найти стажировку или подработку по твоей специальности — "
        "даже если у тебя ещё нет коммерческого опыта.\n\n"
        "📌 *Выбери своё направление обучения:*",
        reply_markup=specialty_keyboard(),
        parse_mode="Markdown"
    )
    await state.set_state(Registration.choosing_specialty)


@router.callback_query(F.data.startswith("spec:"), Registration.choosing_specialty)
async def on_specialty_selected(callback: CallbackQuery, state: FSMContext):
    specialty = callback.data.split(":")[1]
    await state.update_data(specialty=specialty)
    await callback.message.edit_text(
        f"Отлично! Направление: *{SPECIALTY_NAMES.get(specialty, specialty)}*\n\n"
        "📚 Теперь выбери курс:",
        reply_markup=course_keyboard(),
        parse_mode="Markdown"
    )
    await state.set_state(Registration.choosing_course)


@router.callback_query(F.data.startswith("course:"), Registration.choosing_course)
async def on_course_selected(callback: CallbackQuery, state: FSMContext):
    course = int(callback.data.split(":")[1])
    data = await state.get_data()
    specialty = data["specialty"]
    user_id = callback.from_user.id

    # Сохраняем профиль на бэкенде
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{BACKEND_URL}/api/profile",
                json={"user_id": user_id, "specialty": specialty, "course_year": course},
                timeout=5.0
            )
    except Exception:
        pass  # Не блокируем UX при недоступности бэкенда

    await callback.message.edit_text(
        f"✅ Профиль сохранён!\n\n"
        f"• Направление: *{SPECIALTY_NAMES.get(specialty, specialty)}*\n"
        f"• Курс: *{course}*\n\n"
        "Теперь давай разберёмся с твоими навыками и подберём стажировки 👇",
        parse_mode="Markdown"
    )
    await callback.message.answer(
        "Нажми кнопку ниже, чтобы открыть аудит компетенций:",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()


@router.message(F.web_app_data)
async def on_webapp_data(message: Message):
    """Получаем данные из мини-приложения после закрытия."""
    try:
        data = json.loads(message.web_app_data.data)
        skills = data.get("skills", [])
        top_vacancies = data.get("top_vacancies", [])
        missing_skills = data.get("missing_skills", [])

        skills_text = ", ".join(f"`{s}`" for s in skills[:8]) if skills else "_не указаны_"
        missing_text = ", ".join(f"`{s}`" for s in missing_skills[:5]) if missing_skills else "_нет пробелов_ 🎉"

        # Формируем Smart-карточку
        vacancies_text = ""
        for i, vac in enumerate(top_vacancies[:3], 1):
            score = vac.get("match_score", 0)
            vacancies_text += (
                f"{i}. *{vac['title']}* — {vac['company']}\n"
                f"   📍 {vac['location']} | {vac['format']} | "
                f"Совпадение: *{score:.0%}*\n"
            )

        card_text = (
            "🎯 *Твоя карьерная карточка «Первый шаг»*\n\n"
            f"✅ *Твои навыки:* {skills_text}\n\n"
            f"📋 *Подходящие стажировки:*\n{vacancies_text}\n"
            f"📖 *Что подтянуть:* {missing_text}\n\n"
            "_Нажми «Откликнуться» у понравившейся позиции или обнови список завтра — "
            "база вакансий обновляется ежедневно._"
        )
        await message.answer(card_text, parse_mode="Markdown")

    except Exception as e:
        await message.answer("⚠️ Не удалось обработать данные. Попробуй ещё раз.")


@router.message(F.text == "👤 Мой профиль")
async def show_profile(message: Message):
    user_id = message.from_user.id
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/profile/{user_id}", timeout=5.0)
            if resp.status_code == 200:
                profile = resp.json()
                spec = SPECIALTY_NAMES.get(profile.get("specialty", ""), "Не указано")
                course = profile.get("course_year", "?")
                skills = profile.get("skills", [])
                skills_text = ", ".join(f"`{s}`" for s in skills) if skills else "_пройди аудит компетенций_"
                await message.answer(
                    f"👤 *Твой профиль*\n\n"
                    f"🎓 Направление: *{spec}*\n"
                    f"📚 Курс: *{course}*\n"
                    f"💡 Навыки: {skills_text}",
                    parse_mode="Markdown"
                )
            else:
                await message.answer("Профиль не найден. Пройди регистрацию через /start")
    except Exception:
        await message.answer("⚠️ Не удалось загрузить профиль. Попробуй позже.")
