import { useEffect, useState } from "react";
import { bridge } from "./bridge";
import LanguagePage from "./pages/LanguagePage";
import AuditPage from "./pages/AuditPage";
import VacanciesPage from "./pages/VacanciesPage";
import ResultPage from "./pages/ResultPage";
import "./index.css";

type Page = "languages" | "stack" | "vacancies" | "result";

interface ResultData {
  skills: string[];
  top_vacancies: any[];
  missing_skills: string[];
}

export default function App() {
  const [page, setPage] = useState<Page>("languages");
  const [selectedLanguages, setSelectedLanguages] = useState<string[]>([]);
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [result, setResult] = useState<ResultData | null>(null);

  const userId = bridge.getUserId() || 12345;
  const userName = bridge.getUserName();
  const specialty = new URLSearchParams(window.location.search).get("specialty") ?? "it";

  useEffect(() => {
    bridge.init();
    const theme = bridge.getColorScheme();
    document.documentElement.setAttribute("data-theme", theme);
  }, []);

  return (
    <div className="app">
      {page === "languages" && (
        <LanguagePage
          specialty={specialty}
          onNext={(langs) => {
            setSelectedLanguages(langs);
            setPage("stack");
          }}
        />
      )}
      {page === "stack" && (
        <AuditPage
          specialty={specialty}
          selectedLanguages={selectedLanguages}
          onNext={(skills) => {
            setSelectedSkills(skills);
            setPage("vacancies");
          }}
          onBack={() => setPage("languages")}
        />
      )}
      {page === "vacancies" && (
        <VacanciesPage
          userId={userId}
          skills={selectedSkills}
          onNext={(data) => {
            setResult(data);
            setPage("result");
          }}
          onBack={() => setPage("stack")}
        />
      )}
      {page === "result" && result && (
        <ResultPage
          userName={userName}
          skills={result.skills}
          topVacancies={result.top_vacancies}
          missingSkills={result.missing_skills}
          onReset={() => {
            setSelectedLanguages([]);
            setSelectedSkills([]);
            setResult(null);
            setPage("languages");
          }}
        />
      )}
    </div>
  );
}