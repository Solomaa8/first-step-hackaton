import httpx
from aiogram import Router, F
from aiogram.types import Message
from bot.config import BACKEND_URL

router = Router()


@router.message(F.text == "🔔 Обновить вакансии")
async def update_vacancies(message: Message):
    user_id = message.from_user.id
    await message.answer("🔍 Ищу новые стажировки по твоему профилю...")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BACKEND_URL}/api/vacancies/updates/{user_id}",
                timeout=10.0
            )
            if resp.status_code == 200:
                data = resp.json()
                vacancies = data.get("vacancies", [])
                if not vacancies:
                    await message.answer("✅ Новых стажировок пока нет. Загляни завтра!")
                    return
                text = "🆕 *Новые стажировки для тебя:*\n\n"
                for vac in vacancies[:5]:
                    score = vac.get("match_score", 0)
                    text += (
                        f"• *{vac['title']}* — {vac['company']}\n"
                        f"  📍 {vac.get('location','?')} | Совпадение: *{score:.0%}*\n\n"
                    )
                await message.answer(text, parse_mode="Markdown")
            else:
                await message.answer("⚠️ Не удалось получить вакансии. Попробуй позже.")
    except Exception:
        await message.answer("⚠️ Сервис временно недоступен. Попробуй через пару минут.")
