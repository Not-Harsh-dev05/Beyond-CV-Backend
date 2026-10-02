# Assumptions

- No separate attached product document was present in the workspace; this backend follows the product and technical requirements in the task prompt.
- Public registration creates candidate accounts only. Recruiter/admin provisioning is an operator responsibility; allowing public role selection would be privilege escalation.
- Evidence links use GitHub username, Kaggle `competition-slug:team-name`, or certificate verification URL as their source locator.
- Candidate consent is explicit and defaults to false. A candidate may submit/edit profile data before consent but cannot launch ingestion until consent is true.
- Competence is an evidence-source aggregate rather than a validated hiring outcome. The initial source scales are transparent heuristics pending representative labeled outcome data.
- Project originality/tutorial detection is a conservative list of descriptive keyword exclusions plus fork filtering; it is not a learned plagiarism or source-code originality system.
- Role-fit matching is exact case-insensitive word/phrase presence in fetched public repository metadata and README text, not a semantic skill assessment.
- The shipped pedigree CSV is explicitly synthetic and provides only a development fallback. The model output is not representative and is prominently warned until an operator trains it on an approved dataset.
- GitHub account-control proof is a short code in public bio or gist description. Other evidence-source identity proof is partial/unavailable as detailed in DATA_SOURCES.md.
- Kaggle API use requires a candidate-supplied competition/team pair; it does not discover arbitrary user profiles.
- Static certificate HTML parsing is only a preliminary signal, not a cryptographic issuer assertion. Dynamic verification and issuer-specific schemas need future adapters.
- Insights group by GitHub language and positive delta. This is a limited proxy for undervalued skill categories; no protected personal attributes are included in grouping keys.
- Candidate API uses existing numeric user IDs as candidate identifiers; recruiters see only consenting candidate results.
- Docker Compose uses named PostgreSQL/Redis/static volumes, and operators are responsible for secure volume lifecycle and backups.
- Data retention/deletion follows cascade deletion for the candidate account. There is no separate legal hold or audit retention policy implemented.
