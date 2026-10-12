# ParentConnect AI — Testing and Optimization Log

**Student:** Nived Chandrasudan  
**Registration:** 1000521  
**School:** Viraj International School  
**Assessment:** Creating Intelligent Chatbots for Practical Applications

## Test methodology

Test each scenario on the deployed Streamlit app, with **Show matched intents** enabled. Select **New conversation** between different scenarios, but do not reset within a scenario that tests follow-up context. Use only fictional school information. Keep one screenshot per scenario in `evidence/`. Record the actual response and matched intent; do not label untested scenarios as passing.

## Dialogflow console tests (reported by student)

| Scenario | Test | Result | Evidence to upload |
|---|---|---|---|
| Attendance slot filling | "I want attendance details for grade 6" then "Term 1" | Passed, student-reported | `Attendance_SlotFilling.png` |
| Fee context | "What is the tuition fee for grade 8" then "When is it due" | Passed, student-reported | `Fee_Context_Test.png` |
| Fallback | "How do I bake a chocolate cake?" | Passed, student-reported | `Fallback_Test.png` |

These reports describe the Dialogflow console, **not** a completed live Streamlit test.

## Live Streamlit integration tests

**Evidence status:** The student supplied ten screenshots in the conversation, including the five live-streamlit scenarios. The images substantiate the displayed intent names and chatbot replies but are **not yet uploaded to this repository**. They do not establish universal accuracy beyond the tested examples.

| # | Scenario | Exact messages to send | What to check | Actual result / intent | Status | Screenshot |
|---|---|---|---|---|---|---|
| L1 | Attendance | "I want attendance details for grade 6" then "Term 1" | `AttendanceIntent`; asks term; remembers grade; no real student records | Asked for Term 1, remembered Grade 6; matched `AttendanceIntent` | Passed — student-reported | `Live_01_Attendance.png` (saved locally; upload pending) |
| L2 | Exam schedules | "When are the final exams for grade 8?" | `ExamScheduleIntent`; no invented exam dates | Matched `ExamScheduleIntent`; gave Grade 8 final-exam guidance without inventing dates | Passed — student-reported | `Live_02_Exams.png` (saved locally; upload pending) |
| L3 | Fees & context | "What is the tuition fee for grade 8?" then "When is it due?" | `FeeDetailsIntent` followed by `FeeFollowUpIntent`; same context | Both expected intents matched, maintained fee context | Passed — student-reported | `Live_03_Fees.png` (saved locally; upload pending) |
| L4 | Transport & context | "Tell me about bus route 1" then "What about pickup?" | Transport intent and an appropriate contextual follow-up; no invented timings | Matched `TransportRoutesIntent` (83% confidence) then `TransportFollowUpIntent` (58% confidence); **route 1 was labelled Route A** | Functional pass with naming issue — screenshot reviewed | `Live_04_Transport.png` (provided in conversation; GitHub upload pending) |
| L5 | Fallback | "How do I bake a chocolate cake?" | `Default Fallback Intent`; helpful redirection to supported school topics | Matched `Default Fallback Intent`; appropriate fallback response | Passed — student-reported | `Live_05_Fallback.png` (saved locally; upload pending) |
| L6 (optional) | Announcements | "What are the latest school announcements?" | `AnnouncementsIntent`; directs to official current circulars, no fabricated announcements | Record after test | Pending | `Live_06_Announcements.png` |

The student subsequently reported that the live Grade 8 final-exam test matched `ExamScheduleIntent` and saved its screenshot. The screenshot has not yet been uploaded for independent review.

## Confirmed optimization: interface readability

| Date | Problem identified | Change | Verification |
|---|---|---|---|
| 2026-10-13 | Very low text contrast in Streamlit: dark-theme text inherited on light backgrounds | Added `.streamlit/config.toml` with a matching light theme and readable dark text | Student confirmed the website now looks correct and all text is readable |

## New optimization finding from screenshots

The user asked for **bus route 1**, but the response displayed **Route A** (see live transport image). The `@bus_route` entity canonicalizes some number-word variants to lettered routes. Check the official demo naming scheme; if numeric routes are intended, edit the `@bus_route` entity values/synonyms and responses, retrain, then retest the route enquiry. Avoid claiming that Route 1 and Route A are the same real bus service without verification. The follow-up intent works but had 58% reported confidence, suggesting more varied training phrases may help.

## Add any further errors and refinements

| Date | Scenario | Observed problem | Change to intent/entity/phrase/response | Retest result |
|---|---|---|---|---|
| 2026-10-13 | Transport route naming | Input "route 1" shown as "Route A" | Entity normalization / response-label correction recommended, not yet implemented | Retest pending |

## Final performance summary

**As reported by the student; screenshots await upload:**
- Required live scenarios attempted: **5**
- Live scenarios with functional, appropriate intent handling: **5** (one has a route-label mismatch)
- Functional workflow success: **5 / 5** in the supplied examples; **4 / 5** showed no obvious terminology issue. Not an estimate of overall chatbot accuracy.
- Optimization completed and retested: **Streamlit readability/theme correction**; student confirmed readable text after the change
- Evidence: **10 screenshots received and reviewed in conversation**, upload to GitHub pending
- Optional announcement scenario: **not tested**

### Limitations and safety

This is a fictional demonstration, not a live school database. Do not collect or publish real student details, fee records, attendance records, or credentials. The chatbot must not invent dates or balances.
