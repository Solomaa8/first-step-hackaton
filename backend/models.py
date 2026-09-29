from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class Specialty(str, Enum):
    IT = "it"
    ECONOMICS = "economics"
    ENGINEERING = "engineering"


class StudentProfile(BaseModel):
    user_id: int
    specialty: Specialty
    course_year: int = 1
    skills: List[str] = []


class StudentProfileCreate(BaseModel):
    user_id: int
    specialty: Specialty
    course_year: int = 1


class SkillCategory(BaseModel):
    id: str
    name: str
    skills: List[str]


class Vacancy(BaseModel):
    id: str
    title: str
    company: str
    location: str
    format: str  # remote / hybrid / office
    required_skills: List[str]
    description: str
    url: Optional[str] = None
    is_internship: bool = True
    match_score: Optional[float] = None
    missing_skills: Optional[List[str]] = None


class MatchResult(BaseModel):
    matched_vacancies: List[Vacancy]
    related_vacancies: List[Vacancy]
    profile_skills: List[str]
    top_missing_skills: List[str]
    avg_match_score: float


class ResumeCard(BaseModel):
    user_id: int
    full_name: str
    specialty: str
    course_year: int
    skills: List[str]
    top_vacancies: List[Vacancy]
    missing_skills: List[str]
    generated_at: str


class ProfileUpdateSkills(BaseModel):
    user_id: int
    skills: List[str]
