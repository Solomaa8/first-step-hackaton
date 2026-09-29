from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.api import profile, skills, vacancies, resume

app = FastAPI(
    title="Первый шаг — Career Navigator API",
    description="BFF для чат-бота и мини-приложения MAX. Карьерный навигатор для студентов.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router)
app.include_router(skills.router)
app.include_router(vacancies.router)
app.include_router(resume.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "first-step-backend"}
