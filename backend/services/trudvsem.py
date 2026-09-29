import os
import httpx
import logging
from typing import List, Dict, Optional
from backend.mock_data import MOCK_VACANCIES

logger = logging.getLogger(__name__)

TRUDVSEM_BASE = "https://trudvsem.ru/opendata/api/1.0"
USE_MOCK = os.getenv("USE_LOCAL_MOCK", "false").lower() == "true"


async def fetch_vacancies(specialty: str, region_code: str = "16") -> List[Dict]:
    """
    Получает стажировки с API «Работа России».
    При ошибке или USE_LOCAL_MOCK=true — возвращает fallback mock-данные.
    region_code=16 — Республика Татарстан (пилот в Казани).
    """
    if USE_MOCK:
        logger.info("USE_LOCAL_MOCK=true, используем mock-данные")
        return _filter_mock(specialty)

    SPECIALTY_KEYWORDS = {
        "it": ["программист", "разработчик", "тестировщик", "системный администратор", "data"],
        "economics": ["бухгалтер", "экономист", "маркетолог", "аналитик", "менеджер"],
        "engineering": ["инженер", "конструктор", "технолог", "механик"],
    }
    keywords = SPECIALTY_KEYWORDS.get(specialty, ["стажёр"])

    try:
        params = {
            "regionCode": region_code,
            "vacancyType": "INTERNSHIP",
            "experience": "NO_EXPERIENCE",
            "limit": 50,
        }
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(f"{TRUDVSEM_BASE}/vacancies", params=params)
            resp.raise_for_status()
            raw = resp.json()
            items = raw.get("results", {}).get("vacancies", [])
            normalized = [_normalize(v) for v in items]
            filtered = [
                v for v in normalized
                if any(kw.lower() in v["title"].lower() for kw in keywords)
            ]
            if filtered:
                return filtered
            return normalized[:20]  # Если фильтр пустой — вернуть первые 20
    except Exception as e:
        logger.warning(f"Ошибка API trudvsem.ru: {e}. Переключаемся на mock-данные.")
        return _filter_mock(specialty)


def _normalize(raw_vac: Dict) -> Dict:
    """Нормализует поле вакансии из формата API trudvsem.ru."""
    vacancy = raw_vac.get("vacancy", raw_vac)
    return {
        "id": str(vacancy.get("id", "")),
        "title": vacancy.get("duty", "Без названия"),
        "company": vacancy.get("company", {}).get("name", "Не указана"),
        "location": vacancy.get("addresses", {}).get("address", [{}])[0].get("location", "Не указано"),
        "format": "office",
        "required_skills": [],
        "description": vacancy.get("requirement", {}).get("qualification", ""),
        "url": f"https://trudvsem.ru/vacancy/{vacancy.get('id', '')}",
        "is_internship": True,
        "is_mock": False,
    }


def _filter_mock(specialty: str) -> List[Dict]:
    """Фильтрует mock-вакансии по специальности студента."""
    SPECIALTY_MAP = {
        "it": ["python", "javascript", "html", "sql", "git", "testing", "linux"],
        "economics": ["excel", "1c", "smm", "analytics", "accounting"],
        "engineering": ["autocad", "solidworks", "arduino", "cnc", "drawing"],
    }
    target_skills = set(SPECIALTY_MAP.get(specialty, []))
    result = []
    for vac in MOCK_VACANCIES:
        req = set(vac.get("required_skills", []))
        if req & target_skills:
            result.append(vac)
    return result if result else MOCK_VACANCIES
