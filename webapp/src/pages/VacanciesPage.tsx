import { useState, useEffect } from "react";
import { bridge } from "../bridge";

interface Vacancy {
  id: string;
  title: string;
  company: string;
  location: string;
  format: string;
  match_score: number;
  missing_skills: string[];
  required_skills: string[];
  description: string;
  url?: string;
}

interface Props {
  userId: number;
  skills: string[];
  onNext: (result: { skills: string[]; top_vacancies: Vacancy[]; missing_skills: string[] }) => void;
  onBack: () => void;
}

export default function VacanciesPage({ userId, skills, onNext, onBack }: Props) {
  const [matched, setMatched] = useState<Vacancy[]>([]);
  const [related, setRelated] = useState<Vacancy[]>([]);
  const [missingSkills, setMissingSkills] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("all");
  const [saved, setSaved] = useState<Set<string>>(new Set());
  const [showRelated, setShowRelated] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams({
      user_id: String(userId),
      skills: skills.join(","),
    });
    fetch(`/api/vacancies?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setMatched(data.matched_vacancies ?? []);
        setRelated(data.related_vacancies ?? []);
        setMissingSkills(data.top_missing_skills ?? []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [userId, skills]);

  const filteredMatched = filter === "all" ? matched : matched.filter((v) => v.format === filter);
  const filteredRelated = filter === "all" ? related : related.filter((v) => v.format === filter);

  const getScoreClass = (score: number) => {
    if (score >= 0.7) return "score--high";
    if (score >= 0.4) return "score--mid";
    return "score--low";
  };

  const toggleSave = (id: string) => {
    bridge.hapticLight();
    setSaved((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const handleFinish = () => {
    bridge.hapticSuccess();
    onNext({ skills, top_vacancies: matched.slice(0, 5), missing_skills: missingSkills });
  };

  const renderVacancy = (vac: Vacancy) => (
    <div key={vac.id} className="vacancy-card fade-in">
      <div className="vacancy-card__header">
        <div className="vacancy-card__title">{vac.title}</div>
        <div className={`vacancy-card__score ${getScoreClass(vac.match_score)}`}>
          {Math.round(vac.match_score * 100)}%
        </div>
      </div>
      <div className="vacancy-card__company">
        🏢 {vac.company} · 📍 {vac.location} · {vac.format === "remote" ? "🏠 Удалённо" : vac.format === "hybrid" ? "🔄 Гибрид" : "🏛️ Офис"}
      </div>
      <div className="vacancy-card__tags">
        {vac.required_skills.slice(0, 6).map((s) => (
          <span
            key={s}
            className={`tag ${vac.missing_skills.includes(s) ? "tag--missing" : "tag--match"}`}
          >
            {vac.missing_skills.includes(s) ? "✗ " : "✓ "}{s}
          </span>
        ))}
      </div>
      <div className="vacancy-card__actions">
        {vac.url && (
          <a
            href={vac.url}
            target="_blank"
            rel="noopener noreferrer"
            className="vacancy-card__btn vacancy-card__btn--open"
            onClick={(e) => e.stopPropagation()}
          >
            Открыть ↗
          </a>
        )}
        <button
          className={`vacancy-card__btn ${saved.has(vac.id) ? "vacancy-card__btn--saved" : "vacancy-card__btn--save"}`}
          onClick={() => toggleSave(vac.id)}
        >
          {saved.has(vac.id) ? "♥ Сохранено" : "♡ Сохранить"}
        </button>
      </div>
    </div>
  );

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
        <div className="header__title">Подходящие вакансии</div>
        <div className="header__subtitle">
          Найдено {matched.length} по твоему языку и стеку
          {related.length > 0 && ` (+${related.length} смежных)`}
        </div>
      </div>

      <div className="steps">
        <div className="step step--done" />
        <div className="step step--done" />
        <div className="step step--active" />
        <div className="step" />
      </div>

      {/* Filters */}
      <div className="filter-bar">
        {[
          { key: "all", label: "Все форматы" },
          { key: "remote", label: "🏠 Удалённо" },
          { key: "hybrid", label: "🔄 Гибрид" },
          { key: "office", label: "🏛️ Офис" },
        ].map((f) => (
          <button
            key={f.key}
            onClick={() => { bridge.hapticLight(); setFilter(f.key); }}
            className={`filter-btn ${filter === f.key ? "filter-btn--active" : ""}`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Missing skills gap card */}
      {missingSkills.length > 0 && (
        <div className="gap-block">
          <div className="gap-block__title">📚 Прокачай эти навыки для максимального совпадения:</div>
          <div className="gap-block__list">
            {missingSkills.map((s) => (
              <span key={s} className="tag tag--missing">{s}</span>
            ))}
          </div>
        </div>
      )}

      {/* Matched vacancies */}
      {filteredMatched.length === 0 ? (
        <div className="empty">
          <div className="empty__icon">🔍</div>
          <div className="empty__text">По выбранному фильтру подходящих вакансий не найдено</div>
        </div>
      ) : (
        <>
          <div className="section-title">
            ✅ Подходящие по языку
            <span className="section-title__badge">{filteredMatched.length}</span>
          </div>
          {filteredMatched.map(renderVacancy)}
        </>
      )}

      {/* Related vacancies with collapsible section */}
      {filteredRelated.length > 0 && (
        <div className="related-section">
          <button
            className="related-toggle"
            onClick={() => { bridge.hapticLight(); setShowRelated(!showRelated); }}
          >
            <span>🔀 Смежные направления ({filteredRelated.length})</span>
            <span className={`related-toggle__arrow ${showRelated ? "related-toggle__arrow--open" : ""}`}>
              ▼
            </span>
          </button>
          {showRelated && (
            <>
              <div className="related-desc">
                В этих вакансиях совпадает стек (БД, Docker, Git), но требуется другой основной язык.
              </div>
              {filteredRelated.map(renderVacancy)}
            </>
          )}
        </div>
      )}

      {/* Spacer ensuring the last vacancy or related section is completely above the bottom bar */}
      <div className="bottom-bar-spacer" />

      <div className="bottom-bar" style={{ display: "flex", gap: 10 }}>
        <button className="btn btn--secondary" onClick={onBack} style={{ flex: 1 }}>
          ← Стек
        </button>
        <button className="btn btn--gradient" onClick={handleFinish} style={{ flex: 2.2 }}>
          Сформировать отчёт →
        </button>
      </div>
    </div>
  );
}
