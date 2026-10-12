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

| # | Scenario | Exact messages to send | What to check | Actual result / intent | Status | Screenshot |
|---|---|---|---|---|---|---|
| L1 | Attendance | "I want attendance details for grade 6" then "Term 1" | `AttendanceIntent`; asks term; remembers grade; no real student records | Record after test | Pending | `Live_01_Attendance.png` |
| L2 | Exam schedules | "When are the final exams for grade 8?" | `ExamScheduleIntent`; no invented exam dates | Record after test | Pending | `Live_02_Exams.png` |
| L3 | Fees & context | "What is the tuition fee for grade 8?" then "When is it due?" | `FeeDetailsIntent` followed by `FeeFollowUpIntent`; same context | Record after test | Pending | `Live_03_Fees.png` |
| L4 | Transport & context | "Tell me about bus route 1" then "What about pickup?" | Transport intent and an appropriate contextual follow-up; no invented timings | Record after test | Pending | `Live_04_Transport.png` |
| L5 | Fallback | "How do I bake a chocolate cake?" | `Default Fallback Intent`; helpful redirection to supported school topics | Record after test | Pending | `Live_05_Fallback.png` |
| L6 (optional) | Announcements | "What are the latest school announcements?" | `AnnouncementsIntent`; directs to official current circulars, no fabricated announcements | Record after test | Pending | `Live_06_Announcements.png` |

An earlier screenshot shows a live response to a Grade 8 final-exam enquiry, but the matched intent was not displayed. Treat that as preliminary interface evidence, not a finished L2 result.

## Confirmed optimization: interface readability

| Date | Problem identified | Change | Verification |
|---|---|---|---|
| 2026-10-13 | Very low text contrast in Streamlit: dark-theme text inherited on light backgrounds | Added `.streamlit/config.toml` with a matching light theme and readable dark text | Student confirmed the website now looks correct and all text is readable |

## Add any further errors and refinements

| Date | Scenario | Observed problem | Change to intent/entity/phrase/response | Retest result |
|---|---|---|---|---|
| Pending | Pending | Pending | Pending | Pending |

## Final performance summary

Complete **after** testing:
- Live scenarios attempted: ___
- Live scenarios passed: ___
- Pass rate: ___ / ___ = ___%
- Changes made and retested: ___

### Limitations and safety

This is a fictional demonstration, not a live school database. Do not collect or publish real student details, fee records, attendance records, or credentials. The chatbot must not invent dates or balances.
