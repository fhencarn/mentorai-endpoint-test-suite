# Testing Guidelines

## Main rule
Use `IBL.ai.docs` first. Only check `IBL.data.manager` when something is missing, unclear, or inconsistent.

## For every endpoint
Capture:

- Section
- Endpoint
- Method
- Required parameters
- Example payload
- Status code
- Short response summary
- Label
- Doc source
- Notes

## Interpreting results

- `200/201/204` usually means the endpoint worked as expected.
- `400` usually suggests payload or parameter issues.
- `401` usually suggests auth/token problems.
- `403` usually suggests permission or Syracuse tenant restrictions.
- `404` may indicate a bad path, outdated docs, or the wrong server.
- `500+` may indicate a backend issue.

## Consistency
All tests should:

1. Load variables from `.env`
2. Use shared helpers from `utils/`
3. Print status code and summary
4. Save results when useful
5. Assign a consistent label
