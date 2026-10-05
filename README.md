BeyondCV
<p align="center">
  <img src="https://img.shields.io/badge/BeyondCV-Evidence--Based%20Talent%20Discovery-111827?style=for-the-badge" alt="BeyondCV">
</p>

<p align="center">
  <strong>Hire for what people can do, not where they studied.</strong>
</p>

<p align="center">
  An evidence-based talent discovery platform that finds high-potential candidates that résumé screening overlooks.
</p>

<p align="center">
  <strong>Build For Bharat 2.0</strong> · Intelligent Talent and Workforce Ecosystem
</p>

<!-- Technology badges — intentionally placed at the top -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery">
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Sentence--Transformers-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white" alt="Sentence Transformers">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn">
</p>

<p align="center">
  <a href="#the-problem">Problem</a> •
  <a href="#our-solution">Solution</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#how-the-scoring-works">Scoring</a> •
  <a href="#key-features">Features</a> •
  <a href="#tech-stack">Tech Stack</a>
</p>

🏆 The Idea
BeyondCV is built around one simple principle:
A résumé tells you what someone claims. Their work shows you what they can actually do.

Traditional hiring often relies on college tier, previous employer brand and keyword-optimised résumés. BeyondCV adds an evidence layer by analysing publicly verifiable signals such as GitHub projects, Kaggle performance and certificates.
The platform separates demonstrated competence from pedigree, helping recruiters discover candidates whose actual ability may be stronger than their traditional résumé signals suggest.
The Problem
Today's hiring funnel runs heavily on pedigree signals:
- College tier
- Previous employer brand
- Résumé keywords
- Conventional credentials
This creates three problems:
🎯 Talented candidates become invisible
A self-taught developer or a student from a Tier-3 college may have strong projects, open-source contributions and competition results, but can be filtered out before a recruiter sees the evidence.
🔍 Recruiters cannot verify skills at scale
A résumé claims experience, but checking GitHub repositories, competitions and certificates manually for hundreds of applicants is not realistic.
⚖️ Bias gets embedded in screening
Pedigree can become a proxy for ability even though it does not directly measure what a candidate can build.
Our Solution
BeyondCV evaluates what a candidate has actually demonstrated.
	Competence	Pedigree Baseline
Built from	GitHub, Kaggle and verified certificates	College tier and employer brand
Purpose	Measure demonstrated ability	Estimate expected baseline
Answers	“What can this person demonstrably do?”	“What would we expect from their background?”


The Delta
Delta = Competence − Pedigree Baseline
A high positive Delta identifies candidates whose demonstrated competence is significantly above what their traditional background signals might predict.
Architecture
The architecture is intentionally separated into evidence collection, processing, scoring and decision-support layers.
┌──────────────────────────────────────────────────────────────────────┐
│                         1. EVIDENCE SOURCES                         │
│                                                                      │
│   GitHub              Kaggle              Certificates              │
│   Repositories        Competitions       NPTEL / Coursera           │
└───────────────┬───────────────┬────────────────┬────────────────────┘
                │               │                │
                └───────────────┴────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      2. DATA ACQUISITION LAYER                      │
│                                                                      │
│   Fetch public evidence → Verify ownership → Cache external data   │
│                                                                      │
│   • Safe third-party fetching                                       │
│   • SSRF protection                                                 │
│   • Expiring cache                                                  │
│   • Source-failure handling                                        │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       3. DATA PREPARATION                           │
│                                                                      │
│   Filter → Clean → Normalize → Structure                            │
│                                                                      │
│   • Remove/discount forks and tutorial-style projects              │
│   • Normalize evidence to a common 0–100 scale                     │
│   • Label unverified / synthetic evidence                           │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
                 ┌─────────────────────────────────┐
                 │       4. ANALYTICAL LAYER       │
                 │                                 │
                 │  ┌───────────────────────────┐  │
                 │  │ Competence Score          │  │
                 │  │ Evidence-based           │  │
                 │  └─────────────┬─────────────┘  │
                 │                │                │
                 │                ▼                │
                 │  ┌───────────────────────────┐  │
                 │  │ Pedigree Baseline         │  │
                 │  │ College + Employer        │  │
                 │  └─────────────┬─────────────┘  │
                 │                │                │
                 │                ▼                │
                 │  ┌───────────────────────────┐  │
                 │  │ Delta                     │  │
                 │  │ Competence − Baseline     │  │
                 │  └─────────────┬─────────────┘  │
                 │                │                │
                 │                ▼                │
                 │  ┌───────────────────────────┐  │
                 │  │ Role Fit                  │  │
                 │  │ Evidence ↔ Job Skills     │  │
                 │  └───────────────────────────┘  │
                 └────────────────┬────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    5. EXPLAINABLE RANKING                            │
│                                                                      │
│              Role Fit + Delta + Evidence                            │
│                                                                      │
│   Recruiter sees WHY a candidate was surfaced, not just a number.  │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     6. HUMAN DECISION                                │
│                                                                      │
│               Recruiter reviews evidence                             │
│                         ↓                                            │
│                   Hiring decision                                    │
│                                                                      │
│              BeyondCV = Decision Support                              │
│              Not autonomous hiring                                   │
└──────────────────────────────────────────────────────────────────────┘
Architecture in one line
Public Evidence
      ↓
Acquire & Verify
      ↓
Clean & Normalize
      ↓
Competence ───────┐
                  ├──► Delta + Role Fit ───► Explainable Ranking ───► Human Decision
Pedigree Baseline ┘
How the Scoring Works
1. Competence Score
A weighted combination of evidence-source scores.
Evidence with stronger proof of ownership receives greater weight. Substantive projects can receive an additional signal through semantic analysis using sentence embeddings.
2. Pedigree Baseline
A separate regression model uses:
- College tier
- Employer brand
Important: these signals are isolated from the competence score.
3. Delta
Delta = Competence − Pedigree Baseline
A positive Delta means demonstrated competence is above the estimated pedigree baseline.
4. Role Fit
Role Fit measures how many skills required by a target job appear in the candidate's evidence.
5. Explainable Ranking
The ranking combines:
Role Fit + Delta
The recruiter should be able to inspect the evidence behind the result.
Evidence Pipeline
┌───────────────┐
│ GitHub        │
└───────┬───────┘
        │
┌───────▼───────┐
│ Kaggle        │
└───────┬───────┘
        │
┌───────▼───────────┐
│ Certificates      │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│ Evidence Engine   │
│                   │
│ Verify            │
│ Filter            │
│ Normalize         │
│ Weight            │
└────────┬──────────┘
         │
         ▼
┌─────────────────────────┐
│ Candidate Evidence      │
│ Profile                 │
└────────────┬────────────┘
             │
             ├──────────────► Competence Score
             │
             └──────────────► Role Fit
Supported evidence
Source	Evidence
🐙 GitHub	Repositories, activity, READMEs, languages
🏆 Kaggle	Competition leaderboard performance
📜 NPTEL	Certificate verification
📜 Coursera	Certificate verification


Key Features
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
- 🛡️ Protection against server-side request forgery
- ♻️ Graceful third-party source failure handling
Example
Imagine two candidates applying for a Backend Engineer role.
Candidate A
- Tier-1 college
- Strong conventional résumé
- Limited public engineering evidence
Candidate B
- Tier-3 college
- Multiple well-documented Django projects
- Strong GitHub evidence
- Kaggle result in the top 10%
A traditional résumé filter may rank Candidate A higher.
BeyondCV asks:
Who has stronger demonstrated evidence for the actual role?

If Candidate B has stronger role fit and a large positive Delta, BeyondCV can surface Candidate B and show the evidence responsible for the result.
📊 Undervalued Skills Insights
BeyondCV can generate anonymous aggregate views of skills across:
- Regions
- College tiers
- Candidate populations
Small groups are suppressed to reduce the possibility of identifying individuals.
Tech Stack
Layer	Technology
Language	Python
Backend	Django
API	Django REST Framework
Authentication	JWT
Database	PostgreSQL
Async processing	Celery
Cache / message broker	Redis
Machine Learning	scikit-learn
Semantic analysis	sentence-transformers
Data processing	pandas
Containerisation	Docker Compose
Reverse proxy	Nginx
Application server	Gunicorn


Frontend: The final frontend technology should be added once the project stack is fixed.

Real-World Impact
Area	Impact
⚖️ Fairer Hiring	Expands the candidate pool beyond traditional pedigree signals
🔎 Better Talent Discovery	Helps recruiters discover candidates conventional filters may reject
⏱️ Less Manual Screening	Structures evidence that would otherwise require manual checking
🎓 Curriculum Alignment	Shows which skills candidates demonstrate
🔍 Transparency	Makes decision-support outputs easier to explain and audit


🔐 Ethics, Privacy & Fairness
Pedigree Isolation
College and employer information are used for the baseline model only, not competence scoring.
Consent
Candidates should control whether their information is visible to recruiters.
Explainability
Scores should be supported by evidence and understandable reasoning.
Privacy
Aggregate insights should not expose individual candidates.
Human in the Loop
Recruiters make the final hiring decision.
BeyondCV widens the pool of candidates a recruiter considers. It does not make the hiring decision on its own.

⚠️ Security
The platform is designed with safeguards around external data acquisition:
- Safe third-party page fetching
- SSRF protection
- Expiring external-data cache
- Graceful source failure handling
- Candidate consent controls
- Data deletion support
📁 Repository Structure
BeyondCV
│
├── Backend
│   ├── API
│   ├── Data Acquisition
│   ├── Evidence Processing
│   ├── Competence Scoring
│   └── Candidate Ranking
│
└── Frontend
    └── Candidate / Recruiter Interface
🎥 Demo
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
🔮 Future Roadmap
Phase 1 — Stronger Evidence
- Stronger GitHub ownership verification
- Stronger Kaggle verification
- Stronger certificate verification
Phase 2 — Skill Intelligence
- Skill-gap analysis
- Role-specific learning recommendations
- Career recommendations based on market demand
Phase 3 — Fairness & Scale
- Train the baseline on a representative real-world dataset
- Fairness audits of Delta and ranking
- Additional evidence sources such as LeetCode, Codeforces, LinkedIn and research publications
⚠️ Current Limitations
- The pedigree baseline currently relies on a small synthetic sample.
- Competence scoring uses transparent heuristics that require validation against real hiring outcomes.
- Some candidate information may be self-reported.
- Kaggle and certificate ownership verification is currently partial.
These limitations should be addressed before using the system for consequential employment decisions.
💡 Core Philosophy
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
Fairness claims, ranking methodology and Delta values should be validated with representative real-world data before being used in consequential employment decisions.
<p align="center">
  <strong>BeyondCV</strong><br>
  <em>Because talent is everywhere. Opportunity should be too.</em>
</p>