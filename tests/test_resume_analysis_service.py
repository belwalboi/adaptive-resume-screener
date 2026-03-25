from backend.services.resume_analysis_service import ResumeAnalysisService


SOFTWARE_JD = """
Key Responsibilities:
Design, develop, and deploy front-end components using React JS / Ext JS
Build and maintain backend services using Java and Spring Boot
Analyze and resolve support tickets through root-cause analysis and bugfixing
Write optimized SQL queries and ensure data integrity in MySQL databases
Work within a microservices architecture to ensure seamless service communication
Collaborate in an Agile environment using Jira for sprint tracking
Write clean, scalable, and well-tested code and participate in peer reviews
Using AI tools like Github Copilot for best productivity in product development

Skill & Experience Needed:
Strong fundamentals in Java, Object-Oriented Programming, and Data Structures
Working knowledge of React JS / Ext JS and backend development
Basic understanding of Microservices and REST APIs
Experience with SQL/MySQL databases
Good problem-solving skills and learning agility
Strong communication and collaboration skills
"""

DATA_RESUME = """
Experience
Built AI and data analytics projects in Python with SQL and GitHub.

Education
Bachelor of Technology in Computer Science.

Skills
Python, SQL, GitHub, machine learning, data analytics.

Projects
Adaptive resume screener and analytics dashboard projects.

Certifications
Cloud fundamentals certificate.
"""


def test_software_jd_no_longer_scores_as_perfect_ats_match():
    service = ResumeAnalysisService()

    analysis = service.analyze(DATA_RESUME, SOFTWARE_JD)

    assert analysis.ats_score < 100.0
    assert "java" in analysis.missing_keywords
    assert "react" in analysis.missing_keywords
    assert "spring boot" in analysis.missing_keywords
    assert "microservices" in analysis.missing_keywords
    assert "mysql" in analysis.missing_keywords
    assert "vendor ATS score" in analysis.explanation
