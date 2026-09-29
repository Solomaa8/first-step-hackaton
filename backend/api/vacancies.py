from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db, StudentProfileDB
from backend.models import MatchResult, Vacancy
from backend.mock_data import MOCK_VACANCIES
from backend.services.matcher import rank_vacancies, get_top_missing_skills

router = APIRouter(prefix="/api/vacancies", tags=["vacancies"])


@router.get("", response_model=MatchResult)
async def get_vacancies(
    user_id: int = Query(...),
    skills: str = Query(default=""),
    db: Session = Depends(get_db),
):
    profile = db.query(StudentProfileDB).filter_by(user_id=user_id).first()
    specialty = profile.specialty if profile else "it"
    student_skills = skills.split(",") if skills else (profile.skills if profile else [])
    student_skills = [s.strip() for s in student_skills if s.strip()]

    result = rank_vacancies(student_skills, MOCK_VACANCIES)
    matched = result["matched"]
    related = result["related"]

    top_missing = get_top_missing_skills(matched)
    avg_score = sum(v["match_score"] for v in matched) / len(matched) if matched else 0.0

    return MatchResult(
        matched_vacancies=[Vacancy(**v) for v in matched[:20]],
        related_vacancies=[Vacancy(**v) for v in related[:10]],
        profile_skills=student_skills,
        top_missing_skills=top_missing,
        avg_match_score=round(avg_score, 2),
    )


@router.get("/updates/{user_id}")
async def get_vacancy_updates(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfileDB).filter_by(user_id=user_id).first()
    if not profile:
        return {"vacancies": []}
    result = rank_vacancies(profile.skills or [], MOCK_VACANCIES)
    top = [v for v in result["matched"] if v["match_score"] >= 0.5][:5]
    return {"vacancies": top}