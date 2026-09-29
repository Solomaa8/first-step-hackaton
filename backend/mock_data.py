from typing import Dict, List

# === Известные языки программирования ===
KNOWN_LANGUAGES = {
    "python", "javascript", "typescript", "java", "c++", "c#",
    "go", "php", "ruby", "kotlin", "swift", "rust", "scala"
}

# === Мок-вакансии (20+ штук с разными языками) ===
MOCK_VACANCIES: List[Dict] = [
    # --- Python ---
    {
        "id": "mock_001",
        "title": "Стажёр Backend-разработчик (Python)",
        "company": "Яндекс Практикум",
        "location": "Москва",
        "format": "remote",
        "required_skills": ["python", "django", "sql", "git"],
        "description": "Участие в разработке образовательной платформы. Для студентов 3-4 курса.",
        "url": "https://trudvsem.ru/vacancy/mock_001",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_002",
        "title": "Junior Python Developer (FastAPI)",
        "company": "СберТех",
        "location": "Москва",
        "format": "hybrid",
        "required_skills": ["python", "fastapi", "postgresql", "docker", "git"],
        "description": "Разработка микросервисов для внутренних продуктов. Опыт работы с REST API.",
        "url": "https://trudvsem.ru/vacancy/mock_002",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_003",
        "title": "Стажёр Data Analyst",
        "company": "Тинькофф",
        "location": "Москва",
        "format": "hybrid",
        "required_skills": ["python", "sql", "excel", "statistics", "pandas"],
        "description": "Анализ данных, построение отчётов и дашбордов. Работа с командой аналитиков.",
        "url": "https://trudvsem.ru/vacancy/mock_003",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_004",
        "title": "Стажёр в тестирование ПО (QA)",
        "company": "Контур",
        "location": "Екатеринбург",
        "format": "hybrid",
        "required_skills": ["python", "testing", "sql", "postman", "git"],
        "description": "Автоматизация тестирования. Наставничество от QA-инженера.",
        "url": "https://trudvsem.ru/vacancy/mock_004",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_005",
        "title": "ML Engineer Intern",
        "company": "VK",
        "location": "Москва / Санкт-Петербург",
        "format": "hybrid",
        "required_skills": ["python", "pandas", "statistics", "docker", "git"],
        "description": "Работа с моделями машинного обучения в команде рекомендаций.",
        "url": "https://trudvsem.ru/vacancy/mock_005",
        "is_internship": True,
        "is_mock": True
    },
    # --- JavaScript / TypeScript ---
    {
        "id": "mock_006",
        "title": "Стажёр Frontend-разработчик (React)",
        "company": "Авито",
        "location": "Москва",
        "format": "remote",
        "required_skills": ["javascript", "react", "html", "css", "git"],
        "description": "Разработка UI-компонентов для маркетплейса. TypeScript приветствуется.",
        "url": "https://trudvsem.ru/vacancy/mock_006",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_007",
        "title": "Junior Fullstack (Node.js + React)",
        "company": "Ozon Tech",
        "location": "Москва",
        "format": "hybrid",
        "required_skills": ["javascript", "nodejs", "react", "postgresql", "docker"],
        "description": "Fullstack-разработка внутренних инструментов для логистики.",
        "url": "https://trudvsem.ru/vacancy/mock_007",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_008",
        "title": "Стажёр Frontend (Vue.js)",
        "company": "МТС Digital",
        "location": "Москва",
        "format": "remote",
        "required_skills": ["javascript", "vue", "html", "css", "git"],
        "description": "Разработка личного кабинета абонента. Современный стек и менторство.",
        "url": "https://trudvsem.ru/vacancy/mock_008",
        "is_internship": True,
        "is_mock": True
    },
    # --- Java ---
    {
        "id": "mock_009",
        "title": "Стажёр Java-разработчик",
        "company": "Альфа-Банк",
        "location": "Москва",
        "format": "office",
        "required_skills": ["java", "sql", "git", "docker"],
        "description": "Backend-разработка банковских сервисов на Spring Boot.",
        "url": "https://trudvsem.ru/vacancy/mock_009",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_010",
        "title": "Junior Java Developer (Spring)",
        "company": "Ростелеком",
        "location": "Санкт-Петербург",
        "format": "hybrid",
        "required_skills": ["java", "postgresql", "docker", "git", "linux"],
        "description": "Участие в разработке платформы видеонаблюдения. Spring, Kafka.",
        "url": "https://trudvsem.ru/vacancy/mock_010",
        "is_internship": True,
        "is_mock": True
    },
    # --- Go ---
    {
        "id": "mock_011",
        "title": "Стажёр Go-разработчик",
        "company": "VK Cloud",
        "location": "Москва",
        "format": "remote",
        "required_skills": ["go", "docker", "linux", "git", "postgresql"],
        "description": "Разработка облачной инфраструктуры. Микросервисы на Go.",
        "url": "https://trudvsem.ru/vacancy/mock_011",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_012",
        "title": "Junior Backend (Golang)",
        "company": "Wildberries Tech",
        "location": "Москва",
        "format": "hybrid",
        "required_skills": ["go", "sql", "docker", "git"],
        "description": "Высоконагруженные сервисы e-commerce. gRPC, Kafka.",
        "url": "https://trudvsem.ru/vacancy/mock_012",
        "is_internship": True,
        "is_mock": True
    },
    # --- C# ---
    {
        "id": "mock_013",
        "title": "Стажёр C# разработчик (.NET)",
        "company": "Kaspersky",
        "location": "Москва",
        "format": "office",
        "required_skills": ["c#", "sql", "git", "docker"],
        "description": "Разработка серверных компонентов антивирусных решений.",
        "url": "https://trudvsem.ru/vacancy/mock_013",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_014",
        "title": "Junior .NET Developer",
        "company": "1С-Битрикс",
        "location": "Москва",
        "format": "hybrid",
        "required_skills": ["c#", "sql", "git", "postgresql"],
        "description": "Backend-разработка CRM-системы. ASP.NET Core, Entity Framework.",
        "url": "https://trudvsem.ru/vacancy/mock_014",
        "is_internship": True,
        "is_mock": True
    },
    # --- C++ ---
    {
        "id": "mock_015",
        "title": "Стажёр C++ разработчик",
        "company": "Яндекс",
        "location": "Москва",
        "format": "office",
        "required_skills": ["c++", "linux", "git"],
        "description": "Разработка ядра поисковой системы и браузерного движка.",
        "url": "https://trudvsem.ru/vacancy/mock_015",
        "is_internship": True,
        "is_mock": True
    },
    # --- Kotlin ---
    {
        "id": "mock_016",
        "title": "Стажёр Android-разработчик",
        "company": "Сбер",
        "location": "Москва",
        "format": "hybrid",
        "required_skills": ["kotlin", "git", "sql"],
        "description": "Разработка мобильного приложения СберБанк. Jetpack Compose.",
        "url": "https://trudvsem.ru/vacancy/mock_016",
        "is_internship": True,
        "is_mock": True
    },
    # --- PHP ---
    {
        "id": "mock_017",
        "title": "Junior PHP Developer (Laravel)",
        "company": "HeadHunter",
        "location": "Москва",
        "format": "remote",
        "required_skills": ["php", "sql", "html", "css", "git"],
        "description": "Поддержка и развитие крупнейшего job-портала России.",
        "url": "https://trudvsem.ru/vacancy/mock_017",
        "is_internship": True,
        "is_mock": True
    },
    # --- Не-IT вакансии ---
    {
        "id": "mock_018",
        "title": "Помощник системного администратора",
        "company": "РЖД-ИТ",
        "location": "Москва",
        "format": "office",
        "required_skills": ["linux", "networking", "windows_server"],
        "description": "Настройка и поддержка серверной инфраструктуры.",
        "url": "https://trudvsem.ru/vacancy/mock_018",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_019",
        "title": "Ассистент маркетолога (digital)",
        "company": "Ростелеком Digital RT",
        "location": "Москва",
        "format": "remote",
        "required_skills": ["excel", "smm", "analytics", "copywriting"],
        "description": "Помощь в ведении соцсетей, план контента, анализ метрик.",
        "url": "https://trudvsem.ru/vacancy/mock_019",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_020",
        "title": "Стажёр бухгалтер",
        "company": "ООО Городская школа",
        "location": "Москва",
        "format": "office",
        "required_skills": ["1c", "excel", "accounting", "tax_law"],
        "description": "Ведение бухгалтерского учёта, работа в 1С.",
        "url": "https://trudvsem.ru/vacancy/mock_020",
        "is_internship": True,
        "is_mock": True
    },
    {
        "id": "mock_021",
        "title": "Стажёр инженер-конструктор (CAD)",
        "company": "ОКБ Сухой Авиастроения",
        "location": "Москва",
        "format": "office",
        "required_skills": ["autocad", "solidworks", "drawing", "materials_science"],
        "description": "Работа в конструкторском бюро. Чертежи и 3D-моделирование.",
        "url": "https://trudvsem.ru/vacancy/mock_021",
        "is_internship": True,
        "is_mock": True
    },
]

SKILL_CATALOG: Dict[str, Dict] = {
    "it": {
        "name": "Информационные технологии",
        "language_skills": ["python", "javascript", "java", "c++", "c#", "go", "php", "kotlin", "typescript"],
        "categories": [
            {
                "id": "web",
                "name": "🌐 Веб-разработка",
                "skills": ["html", "css", "react", "vue", "nodejs", "django", "fastapi"]
            },
            {
                "id": "data",
                "name": "📊 Данные и БД",
                "skills": ["sql", "postgresql", "mongodb", "excel", "statistics", "pandas"]
            },
            {
                "id": "tools",
                "name": "🛠️ Инструменты",
                "skills": ["git", "docker", "linux", "postman", "vscode", "jira"]
            },
            {
                "id": "qa",
                "name": "✅ Тестирование",
                "skills": ["testing", "selenium", "pytest", "postman", "bug_tracking"]
            },
            {
                "id": "sysadmin",
                "name": "🖧 Сети и администрирование",
                "skills": ["networking", "windows_server", "cisco", "bash"]
            }
        ]
    },
    "economics": {
        "name": "Экономика и бизнес",
        "language_skills": [],
        "categories": [
            {
                "id": "finance",
                "name": "💰 Финансы",
                "skills": ["excel", "1c", "accounting", "tax_law", "financial_analysis"]
            },
            {
                "id": "marketing",
                "name": "📈 Маркетинг",
                "skills": ["smm", "analytics", "copywriting", "seo", "targetolog"]
            },
            {
                "id": "management",
                "name": "📋 Менеджмент",
                "skills": ["project_management", "jira", "agile", "crm", "ms_office"]
            },
            {
                "id": "legal",
                "name": "⚖️ Право и юриспруденция",
                "skills": ["contract_law", "tax_law", "labor_law", "legal_docs"]
            }
        ]
    },
    "engineering": {
        "name": "Инженерия и производство",
        "language_skills": [],
        "categories": [
            {
                "id": "cad",
                "name": "📐 Проектирование CAD",
                "skills": ["autocad", "solidworks", "kompas3d", "revit", "drawing"]
            },
            {
                "id": "materials",
                "name": "📏 Материалы и технологии",
                "skills": ["materials_science", "cnc", "welding", "metrology"]
            },
            {
                "id": "electronics",
                "name": "⚡ Электроника",
                "skills": ["arduino", "raspberry_pi", "soldering", "pcb_design", "matlab"]
            }
        ]
    }
}