from functools import wraps
import hashlib
import hmac
import logging
import os
from distutils.util import strtobool

import requests

from fastapi import HTTPException, Request

from settings import settings


async def verify_signature(request: Request):
    signature_header = request.headers.get("x-hub-signature-256")
    payload_body = await request.body()

    if not signature_header:
        logging.error("'x-hub-signature-256' header is missing.")
        raise HTTPException(
            status_code=403, detail="x-hub-signature-256 header is missing!"
        )

    hash_object = hmac.new(
        settings["secrets"]["token"].encode("utf-8"),
        msg=payload_body,
        digestmod=hashlib.sha256,
    )

    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        logging.error("GitHub signature didn't match.")
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")


def verify_fingerprint():
    if strtobool(os.environ.get("AUTO_UPDATE_FINGERPRINT", "True")):
        response = requests.get("https://api.github.com/meta")
        with open("/root/.ssh/known_hosts", "r+") as known_hosts:
            hosts = ""
            for key in response.json().get("ssh_keys"):
                hosts += f"github.com {key}\n"
            current_host_keys = known_hosts.read()
            known_hosts.seek(0)

            if not current_host_keys:
                logging.warning("GitHub fingerprints not setup. Updating.")
                known_hosts.write(hosts)

            elif hosts and hosts not in current_host_keys:
                logging.warning("GitHub fingerprints have changed. Please verify fingerprints. Auto updating.")
                known_hosts.write(hosts)
                known_hosts.truncate()


def verify(func):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        request: request to get body to verify (request.body()) and header received from GitHub (x-hub-signature-256)
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        """Verify that the payload was sent from GitHub by validating SHA256.

        Raise and return 403 if not authorized.

        Args:
            request: request to get body to verify (request.body()) and header received from GitHub (x-hub-signature-256)
        """

        await verify_signature(kwargs.get('request'))

        verify_fingerprint()

        return await func(*args, **kwargs)

    return wrapper
