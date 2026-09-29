import { bridge } from "../bridge";

interface Vacancy {
  id: string;
  title: string;
  company: string;
  location: string;
  match_score: number;
}

interface Props {
  userName: string;
  skills: string[];
  topVacancies: Vacancy[];
  missingSkills: string[];
  onReset: () => void;
}

export default function ResultPage({ userName, skills, topVacancies, missingSkills, onReset }: Props) {
  const avgScore =
    topVacancies.length > 0
      ? Math.round((topVacancies.reduce((a, v) => a + v.match_score, 0) / topVacancies.length) * 100)
      : 0;

  const handleSendToBot = () => {
    bridge.hapticSuccess();
    bridge.sendDataToBot({
      skills,
      top_vacancies: topVacancies,
      missing_skills: missingSkills,
    });
  };

  return (
    <div className="page-content fade-in">
      <div className="header">
        <div className="header__title">Твоя карта готова!</div>
        <div className="header__subtitle">Отправь результат в бота MAX для получения персонального трека</div>
      </div>

      <div className="steps">
        <div className="step step--done" />
        <div className="step step--done" />
        <div className="step step--done" />
        <div className="step step--active" />
      </div>

      {/* Summary card */}
      <div className="summary-card">
        <div className="summary-card__name">👋 {userName || "Студент"}</div>
        <div className="summary-card__meta">🎯 {skills.length} навыков · 📋 {topVacancies.length} рекомендованных вакансий</div>
        <div className="summary-card__stat">
          <div className="stat-item">
            <div className="stat-item__value">{avgScore}%</div>
            <div className="stat-item__label">Совпадение</div>
          </div>
          <div className="stat-item">
            <div className="stat-item__value">{skills.length}</div>
            <div className="stat-item__label">Твой стек</div>
          </div>
          <div className="stat-item">
            <div className="stat-item__value">{missingSkills.length}</div>
            <div className="stat-item__label">Пробелов</div>
          </div>
        </div>
      </div>

      {/* Top vacancies */}
      <div className="card">
        <div className="section-title" style={{ margin: "0 0 14px" }}>🏆 Лучшие вакансии для тебя</div>
        {topVacancies.map((vac, i) => (
          <div
            key={vac.id}
            style={{
              borderBottom: i < topVacancies.length - 1 ? "1px solid var(--border)" : "none",
              paddingBottom: 12,
              marginBottom: 12,
            }}
          >
            <div style={{ fontWeight: 700, fontSize: 14 }}>
              {i + 1}. {vac.title}
            </div>
            <div style={{ fontSize: 13, color: "var(--text-secondary)", marginTop: 4 }}>
              🏢 {vac.company} · 📍 {vac.location} · <b>{Math.round(vac.match_score * 100)}%</b> совпадение
            </div>
          </div>
        ))}
      </div>

      {/* Missing skills */}
      {missingSkills.length > 0 && (
        <div className="gap-block">
          <div className="gap-block__title">📚 Рекомендуем освоить в первую очередь:</div>
          <div className="gap-block__list">
            {missingSkills.map((s) => (
              <span key={s} className="tag tag--missing">{s}</span>
            ))}
          </div>
        </div>
      )}

      {/* Bottom spacer */}
      <div className="bottom-bar-spacer" />

      <div className="bottom-bar" style={{ display: "flex", gap: 10 }}>
        <button className="btn btn--secondary" onClick={onReset} style={{ flex: 1 }}>
          🔄 Заново
        </button>
        <button className="btn btn--gradient" onClick={handleSendToBot} style={{ flex: 2.2 }}>
          📤 Отправить в MAX
        </button>
      </div>
    </div>
  );
}
