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
  Built for <strong>Build For Bharat 2.0</strong> · Problem Statement: <strong>Intelligent Talent and Workforce Ecosystem</strong>
</p>

<p align="center">
  <a href="#the-problem">The Problem</a> •
  <a href="#our-solution">Our Solution</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#key-features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#impact">Impact</a>
</p>

🏆 The Idea
BeyondCV is designed around a simple principle:
A résumé tells you what someone claims. Their work shows you what they can actually do.

Traditional hiring systems often rely heavily on college tier, previous employer brand and keyword-optimised résumés. BeyondCV adds an evidence layer by analysing publicly verifiable signals such as GitHub projects, Kaggle performance and certificates.
The platform separates demonstrated competence from pedigree, allowing recruiters to discover candidates whose actual ability is stronger than their traditional résumé signals suggest.
The Problem
Today's hiring funnel runs heavily on pedigree signals:
- College tier
- Previous employer brand
- Résumé keywords
- Conventional credentials
This creates a gap on both sides of the market.
🎯 Talented candidates become invisible
A self-taught developer or a student from a Tier-3 college may have strong projects, open-source contributions and competition results, but can be filtered out before a recruiter sees the evidence.
🔍 Recruiters cannot verify skills at scale
A résumé claims experience, but checking GitHub repositories, competitions and certificates manually for hundreds of candidates is not realistic.
⚖️ Bias gets embedded in screening
Pedigree can become a proxy for ability even though it does not directly measure what a candidate can build.
Our Solution
BeyondCV evaluates what a candidate has actually demonstrated.
It separates two concepts:
	Competence	Pedigree Baseline
Built from	Live/public evidence such as GitHub, Kaggle and verified certificates	College tier and employer brand
Answers	“What can this person demonstrably do?”	“What would we expect from their background alone?”


The Delta
Delta = Competence − Pedigree Baseline
A high positive Delta identifies candidates who are performing significantly above what their traditional background signals might predict.
These are exactly the candidates traditional screening can miss.
What Makes BeyondCV Different?
🎓 Pedigree-blind competence scoring
The competence score does not use college or employer information.
College and employer information are isolated to the baseline model.
📊 Evidence over claims
The platform uses public evidence such as:
- GitHub repositories
- GitHub activity
- Kaggle competition performance
- NPTEL certificates
- Coursera certificates
🔎 Explainable scoring
Every score is designed to expose:
- Evidence sources
- Score components
- Relative weights
- Plain-language rationale
🔐 Consent-first
Candidates control whether recruiters can see their information and can request deletion of their data.
⚠️ Honest uncertainty
Unverified evidence receives less weight, while synthetic/sample data is explicitly labelled.
Who Is It For?
Stakeholder	What They Get
👨‍💻 Candidates / Students	A way to demonstrate ability through real work instead of relying only on pedigree
🧑‍💼 Recruiters / Hiring Teams	Explainable, role-specific candidate rankings backed by evidence
🏫 Colleges / Workforce Programs	Privacy-safe aggregate insights into skills and talent trends


How It Works
┌─────────────────────┐
│   Candidate Data    │
│ GitHub • Kaggle •   │
│ Certificates        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Data Acquisition   │
│ Fetch + Verify      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Data Preparation   │
│ Normalize + Filter  │
└──────────┬──────────┘
           │
           ▼
┌────────────────────────────┐
│      Analytical Layer      │
│                            │
│ Competence Score           │
│ Pedigree Baseline          │
│ Delta                      │
│ Role Fit                   │
└──────────┬─────────────────┘
           │
           ▼
┌─────────────────────┐
│ Explainable Ranking │
│ + Candidate Insights│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Recruiter Decision  │
│ Human-in-the-loop   │
└─────────────────────┘
1. Data Acquisition
Candidates link public evidence and the platform collects relevant information.
Source	Evidence Collected
🐙 GitHub	Repositories, activity, READMEs, languages
🏆 Kaggle	Competition leaderboard position
📜 Certificates	NPTEL and Coursera verification pages


2. Data Preparation
The pipeline prepares evidence before scoring:
- Filters forks and tutorial-style repositories
- Normalises different sources to a common 0–100 scale
- Caches external data with expiry
- Reduces unnecessary third-party API requests
- Handles source failures gracefully
3. Analytical Approach
Competence Score
A weighted blend of evidence-source scores.
Proven ownership evidence receives higher weight than unproven evidence, with a small bonus for substantive projects using semantic analysis with sentence embeddings.
Pedigree Baseline
A regression model trained only on:
- College tier
- Employer brand
Delta
Delta = Competence − Pedigree Baseline
Role Fit
Measures how many skills required by a job appear in the candidate's evidence.
Ranking
Candidate ranking combines:
Role Fit + Delta
while keeping the reasoning explainable.
🔥 Key Features
- 🧠 Evidence-based candidate scoring
- 🐙 GitHub evidence analysis
- 🏆 Kaggle performance analysis
- 📜 Certificate evidence
- 📈 Competence vs. pedigree separation
- ➖ Per-candidate Delta score
- 🎯 Role-specific candidate ranking
- 🔐 GitHub ownership verification
- 🤝 Candidate consent controls
- 🗑️ Full data deletion
- 🕵️ Privacy-preserving aggregate insights
- 🛡️ Protection against server-side request forgery
- ♻️ Graceful third-party source failure handling
- 🔍 Explainable scoring instead of a black-box score
🧮 Example
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
BeyondCV asks a different question:
Who has stronger demonstrated evidence for the actual role?

If Candidate B has a high competence score and a large positive Delta, BeyondCV surfaces that candidate and explains which evidence contributed to the result.
📊 Undervalued Skills Insights
BeyondCV can generate anonymous, aggregate views of skills that appear undervalued across:
- Regions
- College tiers
- Candidate populations
Small groups are suppressed to reduce the possibility of identifying individuals.
🌍 Real-World Impact
Area	Impact
⚖️ Fairer Hiring	Gives candidates from lower-tier institutions and smaller regions a stronger way to be evaluated on demonstrated ability
🔎 Better Talent Discovery	Helps recruiters discover candidates conventional filters may reject
⏱️ Less Manual Screening	Replaces repetitive evidence checking with structured, summarised evidence
🎓 Curriculum Alignment	Shows institutions which skills their students demonstrate
🔍 Transparency	Decision-support outputs can be explained and audited


🛠️ Tech Stack
Backend & API
<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Django%20REST%20Framework-A30000?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
</p>

Layer	Technology
Language	Python
Backend	Django
API	Django REST Framework
Authentication	JWT


Database & Async Processing
<p>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery">
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
</p>

Layer	Technology
Database	PostgreSQL
Async processing	Celery
Message broker / cache	Redis


ML / NLP / Data
<p>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Sentence--Transformers-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white" alt="Sentence Transformers">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
</p>

Area	Technology
Machine Learning	scikit-learn
Semantic analysis	sentence-transformers
Data processing	pandas
Regression	scikit-learn


Infrastructure
<p>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn">
</p>

Area	Technology
Containerisation	Docker Compose
Reverse proxy	Nginx
Application server	Gunicorn


Frontend: The current project description does not specify a final frontend technology. Add the actual frontend stack here once it is fixed.

🧩 Technology Overview
                    ┌──────────────────────┐
                    │      Frontend        │
                    │   Candidate / HR UI  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Django REST API    │
                    │        + JWT         │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
       PostgreSQL           Celery              Redis
             │                 │
             │                 ▼
             │        Background ingestion
             │
             └─────────────────┐
                               ▼
                    ┌──────────────────────┐
                    │   ML / NLP Layer     │
                    │                      │
                    │ scikit-learn         │
                    │ sentence-transformers│
                    │ pandas               │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Competence / Delta / │
                    │ Role-Fit / Ranking   │
                    └──────────────────────┘
🔗 Evidence Sources
BeyondCV is designed around evidence that can be checked rather than relying only on résumé claims.
Platform	Evidence
GitHub	Code repositories, activity, languages and project documentation
Kaggle	Competition performance
NPTEL	Certificate verification
Coursera	Certificate verification


🔐 Ethics, Privacy & Fairness
BeyondCV is a decision-support system, not an autonomous hiring system.
Consent by default
Candidate information should not become visible to recruiters without candidate consent.
Right to erasure
Candidates can delete their account and linked data.
Pedigree isolation
College and employer information are used for the baseline model only, not for competence scoring.
Explainability
The system should provide an understandable reason behind its outputs.
Privacy-safe aggregation
Aggregate insights should suppress small groups so individuals cannot be inferred.
Human in the loop
Recruiters make the final hiring decision.
BeyondCV widens the pool of people a recruiter considers. It does not make the hiring decision on its own.

⚠️ Security Considerations
The platform includes safeguards around external data acquisition.
- Safe third-party page fetching
- Protection against server-side request forgery
- Expiring caches for external data
- Graceful handling of failed sources
- Candidate consent controls
- Data deletion support
📁 Repository Structure
The current project documentation identifies separate backend and frontend repositories:
BeyondCV
│
├── Backend
│   ├── API
│   ├── Data ingestion
│   ├── Evidence processing
│   ├── Competence scoring
│   └── Candidate ranking
│
└── Frontend
    └── Candidate / Recruiter interface
🚀 Repositories
Repository	Description
Backend	API, ingestion pipeline, scoring and ranking
Frontend	Candidate and recruiter interface


Add the final repository URLs here once the frontend repository and deployment URLs are fixed.

🎥 Demo
🚧 Demo assets can be added here.

Asset	Link
🎥 Demo Video	<add-link>
🌐 Live Application	<add-link>
📊 Presentation	<add-link>


Screenshots
Candidate Dashboard	Recruiter Ranking	Insights
<screenshot>	<screenshot>	<screenshot>


⚠️ Current Limitations
We want to be transparent about where the project currently stands.
- The pedigree baseline is trained on a small synthetic sample.
- Competence scoring uses transparent heuristics that still need validation against real hiring outcomes.
- College tier and employer information are currently self-reported.
- Kaggle and certificate ownership verification is partial.
🔮 Future Roadmap
Phase 1 — Stronger Evidence
- Stronger Kaggle verification
- Stronger certificate verification
- More robust GitHub ownership verification
Phase 2 — Skill Intelligence
- Skill-gap analysis
- Role-specific learning recommendations
- Career recommendations driven by market demand
Phase 3 — Fairness & Scale
- Train the baseline on a real public dataset
- Fairness audits of Delta and ranking
- More evidence sources
Potential future evidence sources include:
- LeetCode
- Codeforces
- LinkedIn
- Research papers
💡 Core Philosophy
Traditional Hiring:

College → Résumé → Keywords → Shortlist


BeyondCV:

Actual Work
     ↓
Evidence
     ↓
Competence
     ↓
Role Fit + Delta
     ↓
Explainable Shortlist
     ↓
Human Decision
📜 Important Disclaimer
BeyondCV is intended as a decision-support tool.
It should help recruiters discover candidates who might otherwise be overlooked. It should not independently determine whether someone should be hired.
The project's fairness claims and Delta values should be validated with representative real-world data before being used for consequential employment decisions.
<p align="center">
  <strong>BeyondCV</strong><br>
  <em>Because talent is everywhere. Opportunity should be too.</em>
</p>

<p align="center">
  Built with 🐍 Python · Django · PostgreSQL · ML/NLP · Evidence
</p>