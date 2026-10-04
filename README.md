<div align="center">

# BeyondCV

### Hire for what people can do, not where they studied.

An evidence-based talent discovery platform that finds high-potential candidates that résumé screening overlooks.

*Built for **Build For Bharat 2.0** · Problem Statement: **Intelligent Talent and Workforce Ecosystem***

[Demo](#demo) · [The Problem](#the-problem) · [Our Solution](#our-solution) · [How It Works](#how-it-works) · [Impact](#real-world-impact) · [Team](#team)

</div>

---

## The Problem

Today's hiring funnel runs on **pedigree signals**: college tier, previous employer brand and keyword-polished résumés. This creates a gap on both sides of the market:

- **Talented candidates are invisible.** A self-taught developer from a Tier-3 college with strong open-source work is filtered out before anyone sees what they built.
- **Recruiters can't verify skills at scale.** A résumé claims; it doesn't prove. Checking GitHub, competitions and certificates by hand for hundreds of applicants isn't realistic.
- **Bias is built into the process.** Pedigree is a proxy for privilege, not ability. Relying on it narrows the talent pool and reinforces existing inequality.

India produces millions of graduates every year, and most of them don't come from top-tier institutions. Missing them is both an equity problem and a talent-supply problem.

## Our Solution

**BeyondCV** looks at what a person has *actually done* instead of where they come from.

It separates two things that résumés blur together:

| | Competence | Pedigree Baseline |
|---|---|---|
| **Built from** | Live, public evidence: GitHub projects, Kaggle results, verified certificates | College tier and employer brand only |
| **Answers** | *"What can this person demonstrably do?"* | *"What would we expect from their background alone?"* |

The gap between them is the **Delta**:

```
Delta = Competence − Pedigree Baseline
```

A high positive Delta means someone is performing well above what their background predicts. **Those are the candidates traditional screening misses.** BeyondCV surfaces them, and explains why.

### What makes it different

- **Pedigree-blind by design.** The competence score never sees college or employer. The separation is enforced in code, not just in policy.
- **Evidence over claims.** Data is fetched live from public sources, and ownership of the evidence is verified where possible.
- **Explainable, never a black box.** Every score shows its sources, weights and a plain-language rationale.
- **Consent-first.** Candidates control whether recruiters can see them, and can delete everything at any time.
- **Honest about uncertainty.** Unverified evidence counts for less, and synthetic or sample data is always labelled.

## Who It's For

| Stakeholder | What they get |
|---|---|
| **Candidates / students** | A way to be judged on real work. They see their own score, their sources and how their background compares |
| **Recruiters / hiring teams** | Explainable, role-specific rankings that highlight overlooked talent, with evidence they can check |
| **Colleges and workforce programmes** | Aggregate, privacy-safe insights into which skills are undervalued by region and institution tier |

## How It Works

Our pipeline follows the problem-statement flow end to end:

```
Problem → Data Acquisition → Data Preparation → Analytical Approach → Insights → Solution → Impact
```

### 1. Data acquisition
Candidates link public evidence, and we collect it live:

| Source | What we collect |
|---|---|
| **GitHub** | Repositories, activity, READMEs, languages |
| **Kaggle** | Competition leaderboard position |
| **Certificates** | NPTEL and Coursera verification pages |

### 2. Data preparation
- Forks and tutorial-style repositories ("followed along", "bootcamp project") are filtered out
- Each source is normalised to a common 0–100 scale
- Data is cached with an expiry so results stay fresh without hammering third-party APIs

### 3. Analytical approach
- **Competence score:** a weighted blend of source scores, with proven-ownership evidence weighted higher than unproven evidence, plus a small bonus for substantive projects (semantic analysis with sentence embeddings)
- **Pedigree baseline:** a regression model trained only on college tier and employer brand
- **Delta:** competence minus baseline
- **Role fit:** how many of a job's required skills appear in a candidate's evidence
- **Ranking:** a transparent blend of role fit and Delta

### 4. Insights
Anonymous, aggregate views of **undervalued skills** by region and college tier. Small groups are suppressed so no individual can be identified.

### 5. The solution in action

> **Example.** Two candidates apply for a Backend Engineer role. One is from a Tier-1 college with a thin GitHub; the other is from a Tier-3 college with several well-documented Django projects and a Kaggle top-10% finish. A résumé filter ranks the first higher. BeyondCV shows that the second has a large positive Delta and a stronger role-fit, and explains exactly which evidence drove that.

## Key Features

- Evidence-based scoring from GitHub, Kaggle and certificates
- Competence vs. pedigree separation with a per-candidate Delta
- Explainable, role-specific candidate ranking
- GitHub ownership verification through a one-time challenge code
- Candidate consent controls and full data deletion
- Privacy-preserving "undervalued skills" insights
- Safe fetching of third-party pages, with protection against server-side request forgery
- Graceful handling of source failures: one failed source never blocks a score

## Real-World Impact

| Area | Impact |
|---|---|
| **Fairer hiring** | Gives candidates from lower-tier institutions and smaller regions a way to be seen on merit |
| **Better talent discovery** | Helps recruiters find skilled people their usual filters would reject |
| **Less manual screening** | Replaces hand-checking of profiles with verified, summarised evidence |
| **Curriculum alignment** | Shows institutions which in-demand skills their students demonstrate but employers undervalue |
| **Transparency** | Every decision-support output can be explained and audited |

> BeyondCV is a **decision-support tool**. It is meant to widen the pool of people a human recruiter considers, not to make hiring decisions on its own.

## Demo

> 🚧 *Add your demo assets here.*

| | |
|---|---|
| 🎥 Demo video | `<link>` |
| 🌐 Live app | `<link>` |
| 📊 Presentation | `<link>` |

**Screenshots**

| Candidate dashboard | Recruiter ranking | Insights |
|---|---|---|
| `<screenshot>` | `<screenshot>` | `<screenshot>` |

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | `<your frontend stack, e.g. React / Next.js>` |
| **Backend** | Django, Django REST Framework, JWT auth |
| **Async processing** | Celery, Redis |
| **Database** | PostgreSQL |
| **ML / NLP** | scikit-learn, sentence-transformers, pandas |
| **Infra** | Docker Compose, Nginx, Gunicorn |

## Repositories

| Repo | Description |
|---|---|
| **Backend** | `<link to Beyond-CV-Backend>`: API, ingestion pipeline, scoring and ranking. Setup instructions are in its own README |
| **Frontend** | `<link to frontend repo>` |

## Ethics, Privacy and Fairness

- **Consent by default.** Nothing about a candidate is visible to recruiters until they opt in.
- **Right to erasure.** Candidates can delete their account and all linked data.
- **Pedigree isolation.** College and employer data feed the baseline model only, never the competence score.
- **Explainability.** No unexplained scores.
- **Privacy-safe aggregates.** Insights never expose individuals.
- **Human in the loop.** Recruiters make the final call.

## Limitations and Next Steps

We want to be clear about where the project stands.

**Current limitations**
- The pedigree baseline is trained on a small **synthetic** sample. It needs a real, representative dataset before its Delta values are meaningful.
- Competence scoring uses transparent heuristics that haven't yet been validated against real hiring outcomes.
- College tier and employer are self-reported.
- Kaggle and certificate ownership checks are partial.

**Next steps**
- [ ] Train the baseline on a real public dataset
- [ ] Skill-gap analysis: show candidates what to learn for a target role
- [ ] Career recommendations driven by market demand
- [ ] Fairness audits of Delta and ranking
- [ ] Stronger identity verification for Kaggle and certificates
- [ ] More evidence sources (LeetCode, Codeforces, LinkedIn, research papers)


<div align="center">

**BeyondCV** · *Because talent is everywhere. Opportunity should be too.*

</div>
