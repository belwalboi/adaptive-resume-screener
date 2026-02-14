import re
import html
from dataclasses import dataclass

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class AnalysisResult:
    model_features: list[float]
    extracted_features: dict
    ats_score: float
    semantic_score: float
    final_score: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    explanation: str


class ResumeAnalysisService:
    TECH_ALIAS_MAP = {
        "ai": {"ai", "artificial intelligence"},
        "ml": {"ml", "machine learning"},
        "data science": {"data science"},
        "python": {"python"},
        "fastapi": {"fastapi"},
        "r": {"r"},
        "sql": {"sql", "sql query", "nosql"},
        "power bi": {"power bi"},
        "tableau": {"tableau"},
        "sharepoint": {"sharepoint"},
        "excel": {"excel"},
        "powerpoint": {"powerpoint"},
        "numpy": {"numpy"},
        "pandas": {"pandas"},
        "scikit-learn": {"scikit learn", "scikit-learn", "sklearn"},
        "matplotlib": {"matplotlib"},
        "seaborn": {"seaborn"},
        "dspy": {"dspy"},
        "machine learning": {"machine learning"},
        "deep learning": {"deep learning"},
        "computer vision": {"computer vision"},
        "nlp": {"nlp", "natural language processing"},
        "generative ai": {"generative ai", "genai"},
        "llm": {"llm", "large language model", "large language models", "foundation model", "foundation models"},
        "llmops": {"llmops"},
        "rag": {"rag", "retrieval augmented generation", "rag pipelines"},
        "langchain": {"langchain"},
        "langgraph": {"langgraph"},
        "multi-agent systems": {"multi-agent", "multi agent", "ai agents", "agentic ai", "intelligent systems"},
        "docker": {"docker", "containerization"},
        "kubernetes": {"kubernetes"},
        "azure": {"azure", "azure ai", "azure ai foundry", "cosmosdb", "azure cosmosdb"},
        "aws": {"aws"},
        "gcp": {"gcp", "google cloud"},
        "databricks": {"databricks"},
        "spark": {"spark"},
        "cuda": {"cuda"},
        "tensorflow": {"tensorflow", "tensorflow.js", "tensorflowjs"},
        "keras": {"keras"},
        "opencv": {"opencv"},
        "flask": {"flask"},
        "django": {"django"},
        "neo4j": {"neo4j", "graph database", "graph databases"},
        "c++": {"c++"},
        "scala": {"scala"},
        "ci/cd": {"ci/cd", "cicd", "continuous integration", "continuous delivery"},
        "prompt engineering": {"prompt engineering", "context engineering"},
        "statistics": {"statistics", "statistical tests", "probability"},
        "data analytics": {"data analytics", "advanced data analytics", "digital analytics"},
        "github": {"github", "github.com"},
    }

    SECTION_KEYWORDS = {
        "experience": ["experience", "employment", "work history"],
        "education": ["education", "university", "college", "degree"],
        "skills": ["skills", "tech stack", "technologies"],
        "projects": ["projects", "portfolio", "case study"],
        "certifications": ["certification", "certificate", "licensed"],
    }

    EDUCATION_LEVELS = [
        (4, ["phd", "doctorate"]),
        (3, ["master", "m.tech", "mba", "ms"]),
        (2, ["bachelor", "b.tech", "bs", "be"]),
        (1, ["diploma", "associate"]),
    ]

    GITHUB_HINTS = ["github", "pull request", "commit", "open source", "repo"]

    def analyze(self, resume_text: str, job_description: str) -> AnalysisResult:
        resume_lower = self._normalize_text(resume_text)
        jd_lower = self._normalize_text(job_description)

        jd_keywords = self._extract_keywords(jd_lower, is_job_description=True)
        resume_keywords = self._extract_keywords(resume_lower, is_job_description=False)

        matched = sorted(jd_keywords & resume_keywords)
        missing = sorted(jd_keywords - resume_keywords)

        keyword_coverage = (len(matched) / len(jd_keywords)) if jd_keywords else 0.0
        section_score = self._section_score(resume_lower)
        ats_score = round((0.65 * keyword_coverage + 0.35 * section_score) * 100, 2)

        semantic_score = round(self._semantic_similarity(resume_text, job_description), 4)
        skills_match_score = round(keyword_coverage * 100, 2)

        years_experience = float(min(self._extract_years_experience(resume_lower), 60))
        education_level = float(min(self._extract_education_level(resume_lower), 10))
        project_count = float(min(self._extract_projects_count(resume_lower), 100))
        resume_length = float(min(self._extract_resume_length(resume_text), 10000))
        github_activity = float(min(self._extract_github_activity(resume_lower), 10000))

        # Model was originally trained on this exact 6D feature order.
        model_features = [
            years_experience,
            skills_match_score,
            education_level,
            project_count,
            resume_length,
            github_activity,
        ]

        extracted_features = {
            "years_experience": years_experience,
            "skills_match_score": skills_match_score,
            "education_level": education_level,
            "project_count": project_count,
            "resume_length": resume_length,
            "github_activity": github_activity,
        }

        final_score = round((0.55 * skills_match_score) + (0.30 * semantic_score * 100) + (0.15 * ats_score), 2)

        explanation = (
            f"Matched {len(matched)} of {len(jd_keywords)} critical JD keywords. "
            f"ATS section completeness is {round(section_score * 100, 1)}%. "
            f"Semantic alignment score is {semantic_score}."
        )

        return AnalysisResult(
            model_features=model_features,
            extracted_features=extracted_features,
            ats_score=ats_score,
            semantic_score=semantic_score,
            final_score=final_score,
            matched_keywords=matched[:30],
            missing_keywords=missing[:30],
            explanation=explanation,
        )

    def _extract_keywords(self, text: str, is_job_description: bool) -> set[str]:
        keywords: set[str] = set()

        for canonical, aliases in self.TECH_ALIAS_MAP.items():
            if any(self._contains_alias(text, alias) for alias in aliases):
                keywords.add(canonical)

        # Keep "job description keywords" focused and ATS-relevant.
        if is_job_description:
            return keywords

        # Resume fallback: if resume has strong non-stopword token that is also a known alias, include it.
        raw_tokens = re.findall(r"[a-zA-Z0-9+#./-]+", text.lower())
        alias_vocab = {
            token.strip(".,;:!?()[]{}\"'`")
            for aliases in self.TECH_ALIAS_MAP.values()
            for token in aliases
        }
        for token in raw_tokens:
            normalized = token.strip(".,;:!?()[]{}\"'`")
            if len(normalized) < 3:
                continue
            if normalized in ENGLISH_STOP_WORDS:
                continue
            if normalized in alias_vocab:
                keywords.add(normalized)

        return keywords

    def _contains_alias(self, text: str, alias: str) -> bool:
        alias = alias.lower().strip()
        if not alias:
            return False
        # Word-boundary matching avoids accidental substring hits.
        pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
        return re.search(pattern, text) is not None

    def _normalize_text(self, text: str) -> str:
        text = html.unescape(text)
        text = text.lower()
        text = text.replace("&", " and ")
        return re.sub(r"\s+", " ", text).strip()

    def _section_score(self, text: str) -> float:
        hits = 0
        for words in self.SECTION_KEYWORDS.values():
            if any(word in text for word in words):
                hits += 1
        return hits / len(self.SECTION_KEYWORDS)

    def _semantic_similarity(self, resume_text: str, jd_text: str) -> float:
        if not resume_text.strip() or not jd_text.strip():
            return 0.0

        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        matrix = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return max(0.0, min(float(score), 1.0))

    def _extract_years_experience(self, text: str) -> int:
        matches = re.findall(r"(\d{1,2})\+?\s*(?:years|yrs)", text)
        values = [int(m) for m in matches] if matches else [0]
        return max(values)

    def _extract_education_level(self, text: str) -> int:
        for level, keywords in self.EDUCATION_LEVELS:
            if any(keyword in text for keyword in keywords):
                return level
        return 0

    def _extract_projects_count(self, text: str) -> int:
        explicit = re.findall(r"(\d{1,3})\s+projects?", text)
        if explicit:
            return max(int(v) for v in explicit)
        return max(1, min(text.count("project"), 20)) if "project" in text else 0

    def _extract_resume_length(self, text: str) -> int:
        # Training data uses a numeric resume length feature.
        return len(text)

    def _extract_github_activity(self, text: str) -> int:
        score = 0
        for hint in self.GITHUB_HINTS:
            if hint in text:
                score += 120

        repos = len(re.findall(r"github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+", text))
        score += repos * 200
        return score
