# Endpoint Status Matrix

| Section | Endpoint | Method | Doc Source | Status | Label | Response Summary | Notes |
|---------|----------|--------|------------|--------|-------|------------------|-------|
| core | /api/core/heartbeat/celery-beat/ | GET | IBL.ai.docs | 200 | working | Request succeeded | Endpoint returned a valid response |
| core | /api/core/departments/members/check/ | GET | IBL.ai.docs | 400 | working-needs-docs | Request failed due to missing parameters | Check docs for required query parameters |
| core | /api/core/domains/whitelist/ | GET | IBL.ai.docs | 400 | working-needs-docs | Request failed due to missing parameters | Check docs for required query parameters |
| core | /api/core/users/search/ | GET | IBL.ai.docs | 200 | working | Request succeeded | Endpoint returned a valid response |
| core | /api/core/users/proxy/ | GET | IBL.ai.docs | 404 | undocumented | Endpoint not found | Check docs and base path |
| core | /api/core/users/platforms/ | GET | IBL.ai.docs | 400 | working-needs-docs | Missing required parameters | Check docs |
| core | /api/core/users/platforms/config/ | GET | IBL.ai.docs | 400 | working-needs-docs | Missing required parameters | Check docs |
| core | /api/core/users/metadata/proxy/ | GET | IBL.ai.docs | 404 | undocumented | Endpoint not found | Check docs |
| core | /api/core/token/verify/ | GET | IBL.ai.docs | 400 | working-needs-docs | Missing required parameters | Check docs |
| core | /api/core/platforms/syracuse/public-image-assets/ | GET | IBL.ai.docs | 200 | working | Request succeeded | Valid response returned |
| core | /api/core/platform/ | GET | IBL.ai.docs | 400 | working-needs-docs | Missing required parameters | Check docs |
| core | /api/core/platform/config/site/ | GET | IBL.ai.docs | 400 | working-needs-docs | Missing required parameters | Check docs |
| core | /api/core/platform/configurations/public/ | GET | IBL.ai.docs | 400 | working-needs-docs | Missing required parameters | Check docs |
| core | /api/core/platform/configurations/available-settings/ | GET | IBL.ai.docs | 400 | working-needs-docs | Missing required parameters | Check docs |
| core | /api/core/orgs/syracuse/dark-mode-logo/ | GET | IBL.ai.docs | 200 | working | Request succeeded | Image/logo returned |
| core | /api/core/orgs/syracuse/favicon/ | GET | IBL.ai.docs | 200 | working | Request succeeded | Image returned |
| core | /api/core/orgs/syracuse/logo/ | GET | IBL.ai.docs | 200 | working | Request succeeded | Image returned |
| core | /api/core/orgs/syracuse/thumbnail/ | GET | IBL.ai.docs | 200 | working | Request succeeded | Image returned |
| core | /api/core/orgs/syracuse/metadata/ | GET | IBL.ai.docs | 200 | working | Request succeeded | Metadata returned |
| core | /api/core/platform/ | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Likely restricted by role |
| core | /api/core/departments/ | GET | IBL.ai.docs | 200 | working | Request succeeded | No departments returned |
| core | /api/core/departments/members/ | GET | IBL.ai.docs | 400 | working-needs-docs | Missing parameters | Check docs |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/all-chats-memory/ | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Restricted by tenant permissions |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/chat-memory-status/ | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Restricted |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/languages/ | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Restricted |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/memory/ | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Restricted |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/memory-context/ | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Restricted |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/memory-status/ | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Restricted |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/metadata | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Restricted |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/prompt/ | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Restricted |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/prompts/public/ | GET | IBL.ai.docs | 200 | working | Public prompts retrieved | Endpoint accessible |
| ai-prompt | /api/ai-prompt/orgs/syracuse/users/8/styles/ | GET | IBL.ai.docs | 403 | permission-restricted | Access denied | Requires higher permissions |
