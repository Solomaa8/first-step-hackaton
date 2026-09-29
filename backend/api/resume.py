from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db, StudentProfileDB
from backend.models import ResumeCard, Vacancy
from backend.services.trudvsem import fetch_vacancies
from backend.services.matcher import rank_vacancies, get_top_missing_skills

router = APIRouter(prefix="/api/resume", tags=["resume"])

SPECIALTY_NAMES = {
    "it": "Информационные технологии",
    "economics": "Экономика и управление",
    "engineering": "Инженерия и производство",
}


@router.get("/{user_id}", response_model=ResumeCard)
async def get_resume(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfileDB).filter_by(user_id=user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    raw = await fetch_vacancies(profile.specialty)
    ranked = rank_vacancies(profile.skills or [], raw)
    top_vacancies = ranked[:3]
    missing = get_top_missing_skills(ranked, top_n=5)

    return ResumeCard(
        user_id=user_id,
        full_name=f"Студент #{user_id}",
        specialty=SPECIALTY_NAMES.get(profile.specialty, profile.specialty),
        course_year=profile.course_year,
        skills=profile.skills or [],
        top_vacancies=[Vacancy(**v) for v in top_vacancies],
        missing_skills=missing,
        generated_at=datetime.utcnow().isoformat(),
    )
