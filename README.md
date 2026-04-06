# MentorAI Endpoint Test Suite

Shared repository for testing MentorAI-related API endpoints and documenting behavior across Syracuse University permissions.

## Goals

- Validate endpoint functionality
- Separate real bugs from permission issues
- Track documentation mismatches
- Create reusable endpoint test scripts
- Maintain a shared status matrix for the team

## Documentation source rule

- **Primary reference:** `IBL.ai.docs`
- **Secondary reference:** `IBL.data.manager`
- If an endpoint is unclear or missing in the primary source, verify it against the secondary source and note any mismatch.

## Suggested initial scope

Priority sections:

- `ai-mentor`
- `ai-index`
- `ai-analytics`
- `ai-prompt`
- `core`
- `platform`
- `reports`

## Repo structure

```text
mentorai-endpoint-test-suite/
├── README.md
├── requirements.txt
├── .env.example
├── docs/
├── tests/
├── utils/
└── results/
```

## Setup

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your values.
4. Run a test file directly, for example:
   ```bash
   python tests/ai-mentor/test_get_settings.py
   ```

## Standard labels

- `working`
- `working-needs-docs`
- `permission-restricted`
- `syracuse-permission-issue`
- `bad-request`
- `undocumented`
- `deprecated`
- `server-error`
- `unknown`

## Team workflow

For each endpoint tested, record:

- Section
- Endpoint path
- Method
- Doc source
- Status code
- Label
- Response summary
- Notes

## Security notes

- Do **not** commit real API keys, tokens, or personal identifiers.
- Use `.env` locally.
- If sample payloads include IDs, use placeholders.
