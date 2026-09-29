import { useState, useEffect } from "react";
import { bridge } from "../bridge";

interface SkillCategory {
  id: string;
  name: string;
  skills: string[];
}

interface Props {
  specialty: string;
  selectedLanguages: string[];
  onNext: (skills: string[]) => void;
  onBack: () => void;
}

export default function AuditPage({ specialty, selectedLanguages, onNext, onBack }: Props) {
  const [categories, setCategories] = useState<SkillCategory[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/skills/${specialty}`)
      .then((r) => r.json())
      .then((data) => {
        setCategories(data.categories ?? []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [specialty]);

  const toggle = (skill: string) => {
    bridge.hapticSelectionChanged();
    setSelected((prev) => {
      const next = new Set(prev);
      next.has(skill) ? next.delete(skill) : next.add(skill);
      return next;
    });
  };

  const handleNext = () => {
    bridge.hapticSuccess();
    const allSkills = [...selectedLanguages, ...Array.from(selected)];
    onNext(allSkills);
  };

  if (loading) {
    return (
      <div className="loader">
        <div className="spinner" />
      </div>
    );
  }

  return (
    <div className="page-content fade-in">
      <div className="header">
        <div className="header__title">Какой стек знаешь?</div>
        <div className="header__subtitle">
          Отметь фреймворки, БД и инструменты — совпадение считается по ним отдельно от языка
        </div>
      </div>

      <div className="steps">
        <div className="step step--done" />
        <div className="step step--active" />
        <div className="step" />
        <div className="step" />
      </div>

      <div className="card">
        <div className="counter" style={{ flexWrap: "wrap", gap: 8 }}>
          <span>Языки: <span className="counter__num">{selectedLanguages.join(", ")}</span></span>
          <span style={{ opacity: 0.4 }}>|</span>
          <span>Выбрано инструментов: <span className="counter__num">{selected.size}</span></span>
        </div>
      </div>

      {categories.map((cat) => (
        <div className="skill-section" key={cat.id}>
          <div className="skill-section__title">{cat.name}</div>
          <div className="skill-grid">
            {cat.skills.map((skill) => (
              <div
                key={skill}
                className={`skill-chip${selected.has(skill) ? " skill-chip--selected" : ""}`}
                onClick={() => toggle(skill)}
              >
                {selected.has(skill) && <span className="skill-chip__check">✓</span>}
                {skill}
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* Spacer to prevent bottom card cutoff */}
      <div className="bottom-bar-spacer" />

      <div className="bottom-bar" style={{ display: "flex", gap: 10 }}>
        <button className="btn btn--secondary" onClick={onBack} style={{ flex: 1 }}>
          ← Назад
        </button>
        <button
          className="btn btn--primary"
          onClick={handleNext}
          style={{ flex: 2.2 }}
        >
          Найти вакансии →
        </button>
      </div>
    </div>
  );
}
