from typing import Any
import httpx

BASE_URL = "http://192.168.103.101:51081/v3/api/v3"

def submit(payload: dict[str, Any]) -> Any:
    print(">>> calling brokerSubmission")
    with httpx.Client(timeout=10.0) as client:
        res = client.post(f"{BASE_URL}/brokerSubmission", json=payload)
    
    print(">>> response received:", res.status_code)

    return res.json()


def get_submission(case_file_version_id: str):
    with httpx.Client(timeout=10.0) as client:
        res = client.get(
            f"{BASE_URL}/submission",
            params={"caseFileVersionId": case_file_version_id, "userTimeZoneOffset": -5}
        )
        return res.json()


def decline(case_file_version_id: str):
    with httpx.Client(timeout=10.0) as client:
        res = client.post(
            f"{BASE_URL}/declineToQuote",
            json={
                "caseFileVersionId": case_file_version_id,
                "userTimeZoneOffset": -5,
                "declineToQuote": {
                    "declinationReason": "NONE",
                    "declinationDescription": "Auto-declined",
                    "stateProvince": "FL"
                }
            }
        )
        return res.json()