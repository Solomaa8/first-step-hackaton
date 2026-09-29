from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db, StudentProfileDB
from backend.models import StudentProfile, StudentProfileCreate, ProfileUpdateSkills

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.post("", response_model=StudentProfile)
def create_or_update_profile(data: StudentProfileCreate, db: Session = Depends(get_db)):
    existing = db.query(StudentProfileDB).filter_by(user_id=data.user_id).first()
    if existing:
        existing.specialty = data.specialty
        existing.course_year = data.course_year
    else:
        existing = StudentProfileDB(
            user_id=data.user_id,
            specialty=data.specialty,
            course_year=data.course_year,
            skills=[],
        )
        db.add(existing)
    db.commit()
    db.refresh(existing)
    return StudentProfile(
        user_id=existing.user_id,
        specialty=existing.specialty,
        course_year=existing.course_year,
        skills=existing.skills or [],
    )


@router.get("/{user_id}", response_model=StudentProfile)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfileDB).filter_by(user_id=user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return StudentProfile(
        user_id=profile.user_id,
        specialty=profile.specialty,
        course_year=profile.course_year,
        skills=profile.skills or [],
    )


@router.patch("/skills", response_model=StudentProfile)
def update_skills(data: ProfileUpdateSkills, db: Session = Depends(get_db)):
    profile = db.query(StudentProfileDB).filter_by(user_id=data.user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile.skills = data.skills
    db.commit()
    db.refresh(profile)
    return StudentProfile(
        user_id=profile.user_id,
        specialty=profile.specialty,
        course_year=profile.course_year,
        skills=profile.skills or [],
    )
