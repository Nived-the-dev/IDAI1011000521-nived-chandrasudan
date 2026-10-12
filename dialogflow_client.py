"""Small, testable bridge to the user's existing Dialogflow ES agent.

NO intent logic is duplicated here. Dialogflow ES performs recognition,
slot filling, context management and response generation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class AgentResponse:
    message: str
    intent: str
    confidence: float
    awaiting_input: bool = False


def validate_configuration(project_id: str, service_account_json: str) -> dict[str, Any]:
    """Check the shape of secrets, without printing them."""
    if not project_id or project_id.startswith("YOUR_"):
        raise ValueError("Set dialogflow_project_id to the actual Google Cloud Project ID.")
    try:
        credentials = json.loads(service_account_json)
    except (ValueError, TypeError) as exc:
        raise ValueError("service_account_json is not valid JSON.") from exc
    if not isinstance(credentials, dict):
        raise ValueError("service_account_json must contain a JSON object.")
    for field in ("type", "client_email", "private_key", "token_uri"):
        if not credentials.get(field):
            raise ValueError(f"The Google service account JSON is missing {field}.")
    if credentials["type"] != "service_account":
        raise ValueError("Use a Google service-account JSON key, not an OAuth client key.")
    return credentials


def parse_dialogflow_result(result: Any) -> AgentResponse:
    """Extract speech and matching details from a Dialogflow ES QueryResult."""
    answer = (getattr(result, "fulfillment_text", "") or "").strip()
    if not answer:
        chunks = []
        for m in getattr(result, "fulfillment_messages", []):
            text_obj = getattr(m, "text", None)
            for line in getattr(text_obj, "text", []) if text_obj is not None else []:
                if line:
                    chunks.append(str(line))
        answer = "\n\n".join(chunks)
    if not answer:
        answer = "I received your message but couldn't create a text reply. Please try rephrasing."
    intent = getattr(getattr(result, "intent", None), "display_name", "") or "Not identified"
    confidence = float(getattr(result, "intent_detection_confidence", 0.0) or 0.0)
    # Dialogflow ES marks a slot-filling prompt with all_required_params_present=False.
    awaiting = getattr(result, "all_required_params_present", True) is False
    return AgentResponse(answer, intent, confidence, awaiting)


def ask_dialogflow(
    project_id: str,
    session_id: str,
    message: str,
    service_account_json: str,
    *,
    client: Any = None,
    query_input_factory: Any = None,
) -> AgentResponse:
    """Send one text turn; the SAME session_id preserves Dialogflow contexts."""
    if not message.strip():
        raise ValueError("Message must not be empty.")
    if len(message) > 500:
        raise ValueError("Please keep messages under 500 characters.")
    if not session_id or len(session_id) > 36:
        raise ValueError("Invalid session ID.")
    credentials_info = validate_configuration(project_id, service_account_json)

    if client is None:
        from google.cloud import dialogflow
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_info(
            credentials_info, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        client = dialogflow.SessionsClient(credentials=credentials)
    if query_input_factory is None:
        from google.cloud import dialogflow

        query_input = dialogflow.QueryInput(
            text=dialogflow.TextInput(text=message, language_code="en")
        )
    else:
        query_input = query_input_factory(message)

    response = client.detect_intent(
        request={
            "session": f"projects/{project_id}/agent/sessions/{session_id}",
            "query_input": query_input,
        },
        timeout=15,
    )
    return parse_dialogflow_result(response.query_result)


def helpful_error(error: Exception) -> str:
    """Return non-sensitive guidance; never render raw cloud exceptions."""
    if isinstance(error, ValueError):
        return str(error)
    name = type(error).__name__
    if name in ("PermissionDenied", "Forbidden"):
        return (
            "Dialogflow refused this service account. Check the Google Cloud project ID, "
            "Dialogflow API access and Dialogflow API Client role for the service account."
        )
    if name in ("Unauthenticated", "RefreshError", "DefaultCredentialsError"):
        return "Google authentication failed. Check the service-account key in Streamlit secrets."
    if name in ("NotFound",):
        return "Dialogflow agent not found. Verify that the Project ID is the one linked to your ES agent."
    if name in ("DeadlineExceeded", "ServiceUnavailable", "RetryError"):
        return "Dialogflow is slow or temporarily unavailable. Please try again."
    return "I couldn't reach Dialogflow. Check the setup guide or your private Streamlit app logs."
