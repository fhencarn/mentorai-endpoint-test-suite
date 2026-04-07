# Endpoint Status Matrix

| Section | Endpoint | Method | Doc Source | Status | Label | Response Summary | Notes |
|---------|----------|--------|------------|--------|-------|------------------|-------|
| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/ | GET | ibl.ai docs | 200 | working | 7 mentor(s) returned | Auth successful; validated endpoint access and returned mentor list with expected structure (count, results) |
| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/{name}/ | GET | ibl.ai docs | 200 | working | Mentor 'Leadership & Involvement MentorAI' retrieved | Validated mentor retrieval by name; returned unique_id=2262954f-95c1-4a9c-8943-bd3e9f58b3df |
| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/custom-instruction/ | GET | ibl.ai docs | 200 | working | Custom instruction retrieved: id=1, about_user=empty, mentor_tone=empty | Validated custom instruction endpoint and returned expected object fields (id, about_user, mentor_tone) |
| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/export-chathistory/ | POST | ibl.ai docs | 200 | working | Export task created; task_id returned | Validated export-chat history worker endpoint and saved TASK_ID=fb68c5be-25e7-4ad5-a087-930d756a86dd to .env |
| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/downloads/tasks/{task_id}/ | GET | ibl.ai docs | 500 | review needed | Unexpected response returned | Manual review recommended |
| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/edx-memory/ | GET | ibl.ai docs | 200 | working | 0 edx memory record(s) returned | Validated paginated EDX memory list endpoint; sample fields present: none |
| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/edx-memory/{id}/ | GET | ibl.ai docs | 200 | no data | No EDX memory records available to test ID endpoint | List endpoint returned count=0; ID-based test skipped |
| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/free-usage-count | GET | ibl.ai docs | 200 | working | Free usage count returned: 100 | Validated free-usage-count endpoint and returned expected count field |
| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/mentor-feedback/{feedback_id}/ | GET | ibl.ai docs | N/A | blocked | Requires valid feedback_id | No feedback records available in MentorAI UI; endpoint depends on existing feedback data and could not be validated |