import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone

import requests

SIGNING_SECRET = os.environ["SIGNING_SECRET"]
ACTION_RUN_LINK = os.environ["ACTION_RUN_LINK"]

SUBMISSION_URL = "https://b12.io/apply/submission"

PAYLOAD = {
    "action_run_link": ACTION_RUN_LINK,
    "email": "kupelaphiri2003@gmail.com",
    "name": "Kupela Phiri",
    "repository_link": "https://github.com/kupelaphiri/b12-application",
    "resume_link": "https://drive.google.com/file/d/1aaJbhgMat4fBupuf3fopGZPNhZZgIe4d/view?usp=sharing",
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z",
}

# Canonicalise: compact separators, keys sorted alphabetically, UTF-8 encoded
body = json.dumps(PAYLOAD, separators=(",", ":"), sort_keys=True).encode("utf-8")

# HMAC-SHA256 signature
signature = hmac.new(
    SIGNING_SECRET.encode("utf-8"),
    body,
    hashlib.sha256,
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}",
}

print("Submitting application to B12...")
print(f"Payload: {body.decode('utf-8')}")
print(f"Signature: sha256={signature}")

response = requests.post(SUBMISSION_URL, data=body, headers=headers)

print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ Submission successful!")
    print(f"Receipt: {data.get('receipt')}")
else:
    print(f"\n❌ Submission failed with status {response.status_code}")
    sys.exit(1)
