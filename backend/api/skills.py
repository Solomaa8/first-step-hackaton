from fastapi import APIRouter
from backend.mock_data import SKILL_CATALOG

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("/{specialty}")
def get_skills(specialty: str):
    catalog = SKILL_CATALOG.get(specialty)
    if not catalog:
        return {"categories": [], "language_skills": []}
    return catalog