from typing import List, Dict, Tuple, Set
from backend.mock_data import KNOWN_LANGUAGES


def extract_languages(skills: List[str]) -> Set[str]:
    """Извлекает языки программирования из списка навыков."""
    return {s.lower().strip() for s in skills} & KNOWN_LANGUAGES


def extract_stack(skills: List[str]) -> Set[str]:
    """Извлекает стек-навыки (без языков) из списка навыков."""
    return {s.lower().strip() for s in skills} - KNOWN_LANGUAGES


def compute_stack_match(student_skills: List[str], vacancy: Dict) -> Tuple[float, List[str]]:
    """
    Считает Stack Match Score — только по стеку (без языка).
    Возвращает: (score 0.0-1.0, список недостающих навыков стека).
    """
    student_stack = extract_stack(student_skills)
    required_all = set(s.lower().strip() for s in vacancy.get("required_skills", []))
    required_stack = required_all - KNOWN_LANGUAGES

    if not required_stack:
        return 0.5, []

    matched = student_stack & required_stack
    missing = list(required_stack - student_stack)
    score = len(matched) / len(required_stack)
    return round(score, 2), missing


def check_language_match(student_skills: List[str], vacancy: Dict) -> bool:
    """
    Проверяет, совпадает ли хотя бы один язык студента
    с языками вакансии. Если вакансия не требует языков — True.
    """
    student_langs = extract_languages(student_skills)
    vacancy_langs = extract_languages(vacancy.get("required_skills", []))

    if not vacancy_langs:
        return True

    return bool(student_langs & vacancy_langs)


def rank_vacancies(student_skills: List[str], vacancies: List[Dict]) -> Dict:
    """
    Разделяет вакансии на два списка:
    - matched: язык совпал, отсортированы по stack score
    - related: стек похож, но язык другой
    """
    matched = []
    related = []

    for vac in vacancies:
        score, missing = compute_stack_match(student_skills, vac)
        enriched = {**vac, "match_score": score, "missing_skills": missing}

        if check_language_match(student_skills, vac):
            matched.append(enriched)
        elif score > 0:
            related.append(enriched)

    matched.sort(key=lambda v: v["match_score"], reverse=True)
    related.sort(key=lambda v: v["match_score"], reverse=True)

    return {"matched": matched, "related": related[:10]}


def get_top_missing_skills(vacancies: List[Dict], top_n: int = 5) -> List[str]:
    """
    Среди всех вакансий находит часто встречающиеся недостающие навыки.
    """
    freq: Dict[str, int] = {}
    for vac in vacancies:
        for skill in vac.get("missing_skills", []):
            freq[skill] = freq.get(skill, 0) + 1
    sorted_skills = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [s for s, _ in sorted_skills[:top_n]]