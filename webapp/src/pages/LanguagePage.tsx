import { useState, useEffect } from "react";
import { bridge } from "../bridge";

const LANG_ICONS: Record<string, string> = {
  python: "🐍",
  javascript: "⚡",
  typescript: "🔷",
  java: "☕",
  "c++": "⚙️",
  "c#": "🟣",
  go: "🐹",
  php: "🐘",
  kotlin: "🎯",
  rust: "🦀",
  swift: "🦅",
};

interface Props {
  specialty: string;
  onNext: (languages: string[]) => void;
}

export default function LanguagePage({ specialty, onNext }: Props) {
  const [languages, setLanguages] = useState<string[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/skills/${specialty}`)
      .then((r) => r.json())
      .then((data) => {
        setLanguages(data.language_skills ?? []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [specialty]);

  const toggle = (lang: string) => {
    bridge.hapticSelectionChanged();
    setSelected((prev) => {
      const next = new Set(prev);
      next.has(lang) ? next.delete(lang) : next.add(lang);
      return next;
    });
  };

  const handleNext = () => {
    bridge.hapticSuccess();
    onNext(Array.from(selected));
  };

  if (loading) {
    return (
      <div className="loader">
        <div className="spinner" />
      </div>
    );
  }

  if (languages.length === 0) {
    onNext([]);
    return null;
  }

  return (
    <div className="page-content fade-in">
      <div className="header">
        <div className="header__title">Выбери свои языки</div>
        <div className="header__subtitle">
          Отметь языки, на которых пишешь код. Вакансии будут отфильтрованы строго по ним.
        </div>
      </div>

      <div className="steps">
        <div className="step step--active" />
        <div className="step" />
        <div className="step" />
        <div className="step" />
      </div>

      <div className="card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div className="counter">
          Выбрано языков: <span className="counter__num">{selected.size}</span>
        </div>
        {selected.size === 0 && (
          <span style={{ fontSize: 12, color: "var(--warning)", fontWeight: 600 }}>
            Выбери хотя бы 1
          </span>
        )}
      </div>

      <div className="lang-grid">
        {languages.map((lang) => (
          <div
            key={lang}
            className={`lang-card${selected.has(lang) ? " lang-card--selected" : ""}`}
            onClick={() => toggle(lang)}
          >
            {selected.has(lang) && <div className="lang-card__check">✓</div>}
            <div className="lang-card__icon">
              {LANG_ICONS[lang] || "💻"}
            </div>
            <div className="lang-card__name">{lang}</div>
          </div>
        ))}
      </div>

      {/* Spacer so no card is hidden behind bottom bar on any screen */}
      <div className="bottom-bar-spacer" />

      <div className="bottom-bar">
        <button
          className="btn btn--primary"
          onClick={handleNext}
          disabled={selected.size === 0}
        >
          {selected.size > 0 ? `Продолжить к стеку (${selected.size}) →` : "Выбери хотя бы 1 язык"}
        </button>
      </div>
    </div>
  );
}
