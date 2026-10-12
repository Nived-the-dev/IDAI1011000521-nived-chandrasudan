# ParentConnect AI — Deployment and Assessment Guide

## Current working setup (student confirmed)

- Dialogflow ES agent: `ParentConnect_AI_Nived`, connected to Google Cloud project `fleetfix-ai-stpx`
- Dialogflow API: enabled
- Service account: `parentconnect-streamlit` with Dialogflow API Client permission
- Streamlit project files: deployed from GitHub `Nived-the-dev/IDAI1011000521-nived-chandrasudan`
- Streamlit Secrets: configured **in the Streamlit dashboard**, not stored in GitHub
- Streamlit website: student confirmed responses and readable design after a light-theme fix
- **Live Streamlit URL:** student to provide and verify externally

## Secure configuration reference

The app reads `dialogflow_project_id` and `service_account_json` from Streamlit Secrets. **Never commit or share the real key.** An example template with placeholders only:

```toml
dialogflow_project_id = "YOUR_GOOGLE_PROJECT_ID"
service_account_json = '''
PASTE_PRIVATE_SERVICE_ACCOUNT_JSON_HERE
'''
```

After deploying, use **Show matched intents** in the sidebar to verify that a response comes from the Dialogflow API rather than a disconnected interface.

## Testing to finish

Follow [TESTING_LOG.md](TESTING_LOG.md) for at least five varied, realistic *live-site* test scenarios. Preserve screenshots in `evidence/`. Report failures and what was done to fix them; retest before marking Passed. Keep the original three Dialogflow-console screenshots distinct from the new Streamlit tests.

## GitHub documentation to finish

1. Add the **verified public Streamlit app URL** to `README.md`.
2. Check repository includes supporting evidence, agent backup and research report. If not, upload the nonsensitive original project documents.
3. Upload only screenshots with **fictional demo content**; never include Streamlit Secrets, private keys, student records, or Google Cloud authentication.
4. Ensure the full test log reflects what was actually observed.
5. Include a clear explanation of intents, entities, slot filling, context, fallback, limitations and deployment.

## Final assessment PDF

Your school brief requests a PDF containing:
- Student name, candidate registration number, CRS name, course name and school
- GitHub repository URL
- A working live chatbot URL (provide in document as useful additional information)

For stronger evidence, add: project overview, methodology, screenshots, tests and optimization notes. The teacher requires access for `ai.assignments@wacpinternational.org`; clarify whether public repository access is sufficient or whether an invitation is preferred.

## Important cautions

The deployment is an educational demo based on fictitious records and guidance. Do not enter real school records or payment information. Service account JSON must remain private; if ever accidentally exposed, rotate/revoke it immediately.
