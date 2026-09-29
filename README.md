# 🚀 Первый шаг — Карьерный навигатор

Чат-бот с мини-приложением для платформы MAX. Аудит компетенций и подбор стажировок для студентов 1–2 курсов.

---

## 1. Назначение
Помогает студентам без опыта найти профильные стажировки и узнать, какие навыки подтянуть.

## 2. Основной сценарий
`/start` → выбор специальности → аудит навыков в мини-приложении → Skill Match Score → Smart-карточка в чат → отклик в 1 клик.

## 3. Архитектура
- **Bot** (aiogram 3.x) — диалог, кнопка WebApp, Smart-карточка
- **Backend** (FastAPI BFF) — API, Skill Match, интеграция с trudvsem.ru
- **WebApp** (React + Vite) — мини-приложение с MAX Bridge

## 4. Запуск (одна команда)
```bash
cp .env.example .env
# Вставьте MAX_BOT_TOKEN в .env
docker compose up --build -d
```

## 5. Системные требования
- Docker Engine 24+, Docker Compose v2

## 6. Переменные окружения (.env.example)

| Переменная | Описание |
|---|---|
| MAX_BOT_TOKEN | Токен бота от BotFather MAX |
| MAX_BASE_URL | https://api.max.ru |
| WEBAPP_URL | URL мини-приложения (ngrok или продакшн) |
| TRUDVSEM_API_KEY | API-ключ trudvsem.ru (опционально) |
| USE_LOCAL_MOCK | true — использовать локальные данные |

## 7. Порты
| Сервис | Порт |
|---|---|
| Backend (FastAPI) | 8000 |
| WebApp (React/Nginx) | 3000 |

## 8. Зависимости
- Backend: `fastapi`, `uvicorn`, `sqlalchemy`, `httpx`, `pydantic`, `python-dotenv`
- Bot: `aiogram>=3.7`, `httpx`, `python-dotenv`
- WebApp: `react 18`, `recharts`, `vite`

## 9. Внешние сервисы
- [API «Работа России»](https://trudvsem.ru/opendata) — стажировки без опыта (+ автоматический fallback на mock при недоступности)

## 10. Данные и конфиденциальность
Хранятся только обезличенные `user_id` из MAX. Соответствие 152-ФЗ.

## 11. Тестовые данные
```bash
# Переключить на mock-данные (без интернета):
echo "USE_LOCAL_MOCK=true" >> .env
docker compose restart backend
```

## 12. Сценарий проверки (для жюри)
1. Открыть бота → `/start`
2. Выбрать «💻 Информационные технологии» → «1 курс»
3. Нажать «🚀 Пройти аудит компетенций» → открывается мини-приложение
4. Отметить навыки `python`, `git`, `sql` → «Найти стажировки»
5. Убедиться, что вакансии показаны со Skill Match Score (%)
6. Нажать «Сформировать карточку» → «📩 Отправить в MAX»
7. В чате появляется Smart-карточка со списком стажировок

## 13. Пример ответа API
```bash
curl "http://localhost:8000/api/vacancies?user_id=12345&skills=python,git,sql"
# Ответ: {"vacancies": [...], "top_missing_skills": ["docker","linux"], "avg_match_score": 0.67}
```

## 14. Остановка и перезапуск
```bash
docker compose down          # Остановить
docker compose up -d         # Запустить снова
docker compose restart bot   # Перезапустить только бота
```
