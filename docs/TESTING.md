# Testing

The test settings use in-memory SQLite, eager Celery tasks, disabled throttles, and a deterministic embedding stub. Tests must mock all upstream HTTP and DNS. The `make test` target runs pytest with coverage and an 80% minimum threshold; review the terminal coverage summary and investigate uncovered paths instead of relaxing the threshold.

```sh
python -m pip install -r requirements/dev.txt
make test
make lint
```

Coverage focuses on API permissions and envelopes, scorer/pedigree isolation, delta and normalizer formulas, source retry/degradation, SSRF redirect/domain/IP handling, cache/job deduplication, and aggregate k suppression. The test suite must never load or download real embedding weights.
