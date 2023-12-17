import hashlib
import hmac
import os

from fastapi import HTTPException, Request


async def verify_signature(request: Request):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        request: request to get body to verify (request.body()) and header received from GitHub (x-hub-signature-256)
    """

    signature_header = request.headers.get("x-hub-signature-256")
    payload_body = await request.body()

    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")

    hash_object = hmac.new(
        os.environ.get("GITHUB_SECRET_TOKEN").encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256)

    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")
