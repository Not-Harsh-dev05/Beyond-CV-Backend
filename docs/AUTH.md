# Authentication and authorization

JWT uses access/refresh tokens. Refresh rotation is enabled and previous refresh tokens are blacklisted using SimpleJWT's blacklist app. Public registration always creates `CANDIDATE`; there is no client-supplied role field. Provision recruiters/admins through a trusted operator/admin workflow (Django admin or controlled management code), never by changing registration input.

| Capability | Candidate | Recruiter | Admin |
|---|---:|---:|---:|
| Edit own profile and evidence | Yes | No | Full access |
| Delete own account and related records | Yes | No | Full access |
| Ingest own evidence | Yes, with consent | No | Full access |
| View own score | Yes | N/A | Yes |
| View another candidate's score | No | Yes, only with consent | Yes |
| Create job roles | No | Yes | Yes |
| View job rankings | No | Yes, consenting candidates only | Yes |
| View aggregate insights | No | No | Yes |
| Retrain pedigree model | No | No | Yes |

Object-level checks run in addition to role checks for owned candidate evidence and jobs. Recruiter routes filter `consent_given=True`. Candidate deletion cascades through profile, links, snapshots, ingestion jobs, and scores. Authentication routes have a stricter 10/minute throttle; general limits vary by role.

Set a unique `SECRET_KEY`, production `ALLOWED_HOSTS`, restricted `CORS_ALLOWED_ORIGINS`, and secure HTTPS proxy settings before deployment. No credential or token is returned in API errors or written to structured logs.
