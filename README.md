BeyondCV
<p align="center">
  <img src="https://img.shields.io/badge/BeyondCV-Evidence--Based%20Talent%20Discovery-111827?style=for-the-badge" alt="BeyondCV">
</p>

<p align="center">
  <strong>Hire for what people can do, not where they studied.</strong>
</p>

<p align="center">
  BeyondCV is an evidence-based talent discovery platform designed to help recruiters discover high-potential candidates who may be overlooked by traditional résumé screening.
</p>

<p align="center">
  Built for <strong>Build For Bharat 2.0</strong> · Problem Statement: <strong>Intelligent Talent and Workforce Ecosystem</strong>
</p>

🎯 The Problem
Traditional hiring often depends heavily on:
- College tier
- Previous employer brand
- Résumé keywords
- Conventional credentials
This can create two major problems:
1. Strong candidates can be overlooked because their institution or résumé does not carry enough pedigree.
2. Recruiters cannot manually verify evidence at scale across GitHub, competitions, certificates, and other public sources.
A candidate's background is not the same thing as their demonstrated ability.
💡 Our Solution
BeyondCV evaluates evidence of what a candidate has actually done.
Instead of relying only on résumé claims, the platform analyses public evidence such as:
- GitHub repositories and activity
- Kaggle competition performance
- NPTEL certificates
- Coursera certificates
The system separates demonstrated competence from pedigree.
Competence vs. Pedigree
	Competence	Pedigree Baseline
Based on	Demonstrated evidence	College tier and employer brand
Purpose	Measure what the candidate can demonstrate	Estimate the expected baseline
Used for	Competence scoring	Baseline comparison


The Delta
Delta = Competence − Pedigree Baseline
A high positive Delta indicates that a candidate's demonstrated competence is significantly stronger than what their traditional background signals might suggest.
This helps surface candidates who traditional screening may overlook.
🔄 How BeyondCV Works
Candidate Evidence
       │
       ▼
Data Acquisition
       │
       ▼
Data Preparation
       │
       ▼
Competence Scoring
       │
       ├──────────────► Pedigree Baseline
       │
       ▼
      Delta
       │
       ▼
Role Fit Analysis
       │
       ▼
Explainable Ranking
       │
       ▼
Human Recruiter Decision
1. Data Acquisition
The platform collects relevant evidence from supported public sources.
Source	Evidence
🐙 GitHub	Repositories, activity, READMEs, languages
🏆 Kaggle	Competition leaderboard performance
📜 NPTEL	Certificate verification
📜 Coursera	Certificate verification


2. Data Preparation
Collected evidence is prepared before scoring:
- Tutorial-style and forked repositories can be filtered.
- Different sources are normalised to a common scale.
- External data can be cached with an expiry.
- Source failures are handled without blocking the entire score.
3. Analytical Layer
BeyondCV calculates:
Competence Score
A weighted combination of evidence-source scores, with stronger ownership evidence receiving greater weight.
Pedigree Baseline
A regression-based baseline using college tier and employer brand.
Delta
Delta = Competence − Pedigree Baseline
Role Fit
Measures how much of a target role's required skill set appears in the candidate's evidence.
Ranking
Combines role fit and Delta while keeping the reasoning explainable.
⭐ Key Features
- 🧠 Evidence-based candidate scoring
- 🐙 GitHub evidence analysis
- 🏆 Kaggle performance analysis
- 📜 Certificate evidence
- 📈 Competence vs. pedigree separation
- ➖ Per-candidate Delta score
- 🎯 Role-specific candidate ranking
- 🔐 GitHub ownership verification
- 🤝 Candidate consent controls
- 🗑️ Data deletion support
- 🔎 Explainable scoring
- 🕵️ Privacy-preserving aggregate insights
- 🛡️ Protection against unsafe third-party fetching
- ♻️ Graceful handling of external-source failures
🧮 Example
Consider two candidates applying for a Backend Engineer role.
Candidate A
- Tier-1 college
- Strong conventional résumé
- Limited public engineering evidence
Candidate B
- Tier-3 college
- Multiple well-documented Django projects
- Strong GitHub evidence
- Strong competition performance
A conventional résumé filter may favour Candidate A.
BeyondCV instead evaluates the evidence.
If Candidate B demonstrates stronger role fit and a high positive Delta, the platform can surface Candidate B and explain which evidence contributed to the result.
🔐 Fairness, Privacy & Ethics
BeyondCV is designed as a decision-support system, not an autonomous hiring system.
Pedigree Isolation
College and employer information are separated from the competence score and used only for the baseline comparison.
Consent
Candidates should control whether their information is available to recruiters.
Explainability
Scores should be supported by evidence and understandable reasoning rather than being an unexplained black box.
Privacy
Aggregate insights should avoid exposing individual candidates.
Human in the Loop
The recruiter remains responsible for the final hiring decision.
BeyondCV widens the pool of candidates a recruiter considers. It does not make the hiring decision by itself.

🛠️ Tech Stack
Backend
<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/Django%20REST%20Framework-A30000?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white">
</p>

Component	Technology
Language	Python
Backend	Django
API	Django REST Framework
Authentication	JWT


Database & Background Processing
<p>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white">
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white">
</p>

Component	Technology
Database	PostgreSQL
Async processing	Celery
Cache / message broker	Redis


ML / NLP
<p>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white">
  <img src="https://img.shields.io/badge/Sentence--Transformers-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white">
</p>

Component	Technology
Machine Learning	scikit-learn
Semantic analysis	sentence-transformers
Data processing	pandas


Infrastructure
<p>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white">
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white">
</p>

Component	Technology
Containerisation	Docker Compose
Reverse proxy	Nginx
Application server	Gunicorn


📊 Impact
Area	Expected Impact
⚖️ Fairer hiring	Expands the pool beyond traditional pedigree signals
🔎 Talent discovery	Helps recruiters find overlooked candidates
⏱️ Screening efficiency	Structures evidence that would otherwise require manual checking
🎓 Workforce insights	Helps identify skills demonstrated across different candidate groups
🔍 Transparency	Makes candidate scoring easier to inspect and explain


🔮 Future Roadmap
Evidence
- Stronger GitHub ownership verification
- Stronger Kaggle verification
- Stronger certificate verification
- Additional evidence sources
Intelligence
- Skill-gap analysis
- Role-specific learning recommendations
- Career recommendations based on market demand
Fairness & Scale
- Train the pedigree baseline on a representative real-world dataset
- Perform fairness audits on Delta and ranking
- Expand evidence sources to platforms such as LeetCode, Codeforces, LinkedIn, and research publications
⚠️ Current Limitations
- The pedigree baseline currently relies on a small synthetic sample.
- Competence scoring uses transparent heuristics that require validation against real hiring outcomes.
- Some candidate information may be self-reported.
- Kaggle and certificate ownership verification is currently partial.
These limitations should be addressed before using the system for consequential employment decisions.
📁 Repository
BeyondCV
│
├── Backend
│   ├── API
│   ├── Data acquisition
│   ├── Evidence processing
│   ├── Competence scoring
│   └── Candidate ranking
│
└── Frontend
    └── Candidate / Recruiter interface
🎥 Demo
Add project assets here:
Asset	Link
🎥 Demo Video	<add-link>
🌐 Live Application	<add-link>
📊 Presentation	<add-link>


Screenshots
Add screenshots of:
- Candidate dashboard
- Recruiter ranking
- Candidate evidence
- Delta / competence explanation
- Aggregate insights
🧠 Core Philosophy
Traditional Hiring

College
   ↓
Résumé
   ↓
Keywords
   ↓
Shortlist


BeyondCV

Actual Work
   ↓
Evidence
   ↓
Competence
   ↓
Role Fit + Delta
   ↓
Explainable Ranking
   ↓
Human Decision
📜 Disclaimer
BeyondCV is a decision-support platform intended to help recruiters discover candidates who may be overlooked by conventional screening.
It should not independently determine whether a candidate should be hired.
Fairness claims, ranking methodology, and Delta values should be validated with representative real-world data before being used in consequential employment decisions.
<p align="center">
  <strong>BeyondCV</strong><br>
  <em>Because talent is everywhere. Opportunity should be too.</em>
</p>

<p align="center">
  Built with 🐍 Python · Django · PostgreSQL · ML/NLP
</p>