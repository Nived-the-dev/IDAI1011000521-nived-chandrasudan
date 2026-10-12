# ParentConnect AI

### A Dialogflow ES–powered school communication assistant · Streamlit web app

**Student:** Nived Chandrasudan  
**Candidate registration number:** 1000521  
**School:** Viraj International School  
**CRS:** Artificial Intelligence  
**Course:** Artificial Intelligence: Real-World Applications and Implications  
**Assessment:** Summative Assessment (Individual) · 60 marks

> **DEMONSTRATION PROJECT — NOT CONNECTED TO LIVE SCHOOL RECORDS.** All school examples are illustrative. Do not enter personal student information. Parents should verify dates, dues, attendance, and contacts through authorized school channels.

## Live chatbot

**Streamlit URL:** [Open the live ParentConnect AI chatbot](https://idai1011000521-nived-chandrasudan-nzdwzhh68kjjnrxbsbuny4.streamlit.app/)  
**Live-site verification:** URL provided by the student, who reports a working chatbot and five passed tests. Independent public access verification is still pending (test the link in a private/incognito browser).  
**Technology:** Dialogflow ES `detectIntent` through its V2 API, Python and Streamlit Community Cloud.

## 1. Project overview

School-parent communication can involve delays and uncertainty when families need answers about attendance, exams, fee information and announcements. ParentConnect AI offers a single easy-to-use interface that recognizes a variety of natural language queries and guides users to reliable official channels for private or time-sensitive information.

**Intended users:** parents/guardians, school communication teams and support staff.  
**Objectives:** quick navigation, clear replies, contextual follow-ups, slot-filling and privacy-aware communication.  
**Out of scope:** real student records, authentication into student portals, payments, officially verified schedules and live school announcements.

## 2. Architecture and integration

```text
Parent / evaluator browser
          |
          v
  Streamlit frontend (app.py)
          |
          v
 Python bridge (dialogflow_client.py)
          |  HTTPS / authenticated Google API call
          v
 Google Dialogflow ES agent
          |  25 intents / 12 custom entities
          v
 Intent match + parameters + session context
          |
          v
 Response displayed by Streamlit
```

The Python backend uses a scoped Google service account with the **Dialogflow API Client** role. `google-cloud-dialogflow` calls `SessionsClient.detect_intent` for every submitted user message. The same 32-character random session ID is reused for the whole conversation so Dialogflow retains contexts between follow-up requests. Clicking **New conversation** creates a different ID. **The app does not replace Dialogflow with hard-coded answers.**

### Security and ethics

- Google service-account credentials are held only in **Streamlit secrets**, not this repository or the browser.
- `.gitignore` blocks `secrets.toml`, commonly named key files and private environment files.
- The app does not store chat transcripts in a database; messages are kept in the Streamlit browser session for the duration of the chat. Google and the hosting provider may process requests and maintain operational logs in accordance with their own services.
- Avoid inputting real student data. A custom viewing password is available as an optional additional safety measure; this is not a replacement for proper school authentication.
- Unknown information is not invented; parents are directed to the official portal / school office.

## 3. Dialogflow intents

The imported ES package saved in `agent_backup/ParentConnect_AI_Dialogflow_ES_Agent.zip` includes **25 intents** and 288 example training utterances in total (the 25 include default welcome and fallback intents). The most important intent roles are listed below.

| Intent | What it handles |
|---|---|
| Default Welcome Intent | Greetings, orientation and suggestion options |
| Default Fallback Intent | Unknown or unrelated questions |
| AttendanceIntent | Requests for class/term attendance; asks for missing grade/term |
| AttendanceDemoExampleIntent | Explicitly fictional 92% Grade 8 attendance example |
| ExamScheduleIntent | Grade and examination type; asks for missing parameters |
| ExamPreparationIntent | Study and examination preparation guidance |
| FeeDetailsIntent | Grade and type of fee; activates `schoolfees_active` context |
| FeeFollowUpIntent | Fee-related follow-ups such as due dates |
| FeePaymentIntent | Safe instructions for official fee payment channels |
| AnnouncementsIntent | School circulars and announcements |
| TransportRoutesIntent | Bus route enquiries; activates transport follow-up context |
| TransportFollowUpIntent | Continued enquiry about previously specified transport route |
| BusTimingIntent | General bus pick-up / drop-off enquiries |
| SchoolTimingsIntent | School hours questions |
| HomeworkIntent | Subject / grade homework queries |
| HolidaysIntent | Academic calendar and school holidays |
| EventsIntent | School events |
| PTMIntent | Parent-teacher meetings |
| SchoolContactIntent | Official contacts |
| TeacherContactIntent | Contact teachers through approved channels |
| ReportCardIntent | Report card guidance and student-record privacy |
| CertificatesIntent | School documents and certificates |
| AdmissionsIntent | New-admission queries |
| LibraryIntent | Library support |
| SchoolUniformIntent | Uniform guidance |

### Custom entities

| Custom entity | Purpose / extracted parameter |
|---|---|
| `@grade` | Class / grade, such as Grade 8 |
| `@academic_term` | Term or school year period |
| `@exam_type` | Exam type, such as finals or midterm |
| `@fee_type` | Tuition / transport / activities / exams |
| `@bus_route` | School transport route |
| `@school_day` | Day of the school week |
| `@school_event` | Types of events / PTM |
| `@homework_subject` | School subject |
| `@document_type` | Report cards, certificates and other documents |
| `@communication_channel` | Phone, email, office and other approved contact paths |
| `@query_topic` | Type of information requested |
| `@section` | Student section, e.g., Section A |

**Slot-filling**: Attendance requires `grade` + `academic_term`; ExamSchedule requires `grade` + `exam_type`; FeeDetails requires `grade` + `fee_type`; other required parameters are defined in the exported Dialogflow package. Dialogflow itself prompts for missing parameters.  
**Context**: `schoolfees_active` is used by FeeFollowUpIntent, and `schooltransport_active` is used by TransportFollowUpIntent.  
**Rich responses**: Dialogflow welcome intent contains suggestion-chip payloads. The Streamlit interface provides its own clickable topic shortcuts so the user experience does not depend on Messenger/Web Demo rendering rich content.

## 4. Design decisions / user research

The project identifies parent difficulties including finding information promptly, keeping track of changing notices, and locating the correct school contact channel. Its intended users are parents and school staff. Design goals: readable conversations, consistent school topics, follow-up clarification, and privacy protection. The problem-research document is provided under `evidence/Step1_Problem_Research.pdf`. It describes **anticipated needs**, not a claim that actual interviews were conducted.

## 5. Files

```text
ParentConnect_Streamlit_Nived/
├── app.py                          # Responsive interface, quick replies and conversation UI
├── dialogflow_client.py            # Secure API request / response handling
├── requirements.txt                # Python dependencies
├── .streamlit/config.toml          # Theme styling
├── .streamlit/secrets.toml.example  # PLACEHOLDER ONLY (no working credentials)
├── .gitignore                      # Secret-file protection
├── agent_backup/                   # Original Dialogflow ES agent backup (ZIP)
├── evidence/                       # Research report + add real screenshots here
├── docs/SETUP_STEP_BY_STEP.md      # Illustrated-by-words deployment walkthrough
├── docs/TESTING_LOG.md             # Test plan and honest record of reported tests
└── tests/                           # Offline bridge unit tests
```

## 6. Deployment instructions

See **[docs/SETUP_STEP_BY_STEP.md](docs/SETUP_STEP_BY_STEP.md)**. Summary:

1. Upload the files into a GitHub repository (without secrets).
2. Configure the *existing* Dialogflow ES agent's Cloud project with its Dialogflow API enabled and a minimally privileged service account.
3. In https://share.streamlit.io/ create a new app: repository = your repo, main file = `app.py`.
4. Set Streamlit **secrets** to `dialogflow_project_id` and `service_account_json` (and optionally a `viewer_password`).
5. Deploy, confirm a user query returns a **real Dialogflow intent name**, run at least five realistic tests and save screenshots.
6. Add the verified live app URL above, finish your SA report PDF, and link this repository in the report.

For local development (optional):

```bash
python -m pip install -r requirements.txt
# Create .streamlit/secrets.toml with your PRIVATE credentials (never commit it)
streamlit run app.py
```

## 7. Testing and optimization

**Already reported by the student in the Dialogflow console:** attendance slot-filling, a contextual fee follow-up, and fallback handling. Associated screenshots were saved locally by the student and still need to be added to the repository if chosen as evidence.

**Not yet verified**: live Streamlit app / actual API integration, performance and accessibility from another device. Follow the pending scenarios and iteration log in **[docs/TESTING_LOG.md](docs/TESTING_LOG.md)**. Record genuine successes and failures, refine the Dialogflow training data, and retest.

Run offline unit tests:

```bash
python -m unittest discover -s tests -v
```

## 8. Limitations and future scope

- Requires Google API permissions and a secure Cloud credential to call an ES agent.
- No live student information, timetable feed, school database or payment gateway is integrated.
- No full parent identity verification; therefore personalized records are intentionally excluded.
- An authorized school version would need identity verification, consent, access controls, verified source data, monitoring and a privacy review.

## 9. References

- [Dialogflow ES — Interactions with the API](https://cloud.google.com/dialogflow/es/docs/quick/api)
- [Dialogflow ES — Access control](https://cloud.google.com/dialogflow/es/docs/access-control)
- [Dialogflow API IAM roles](https://cloud.google.com/iam/docs/roles-permissions/dialogflow)
- [Streamlit — Deploy your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Streamlit — Secrets management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

**Notice:** This repository is an individual student assessment. The interface is educational and is not an official communication service of Viraj International School.
