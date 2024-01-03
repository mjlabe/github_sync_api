import os
import subprocess

import logging

import uvicorn
from fastapi import FastAPI, Request, HTTPException

from settings import settings
from verify_remotes import verify_signature, verify_fingerprint


app = FastAPI()


@app.post("/{repo}/pull")
async def pull_changes(request: Request, repo: str):
    logging.info(f"Client {request.client.host} requested pulling changes for repo '{repo}'")
    # verify request comes from GitHub webhook
    await verify_signature(request)

    # verify GitHub fingerprints are up-to-date
    verify_fingerprint()

    repo = settings["repos"].get(repo)

    if not repo:
        logging.warning(f"Repo {repo} is not defined in settings")
        raise HTTPException(detail="Repo is not defined in settings", status_code=404)

    fetch = subprocess.run(
        ["git", "fetch"], cwd=repo, capture_output=True, text=True
    )
    pull = subprocess.run(
        ["git", "pull"], cwd=repo, capture_output=True, text=True
    )

    logging.info(str({"message": {"fetch": fetch, "pull": pull}}))
    return {"message": {"fetch": fetch, "pull": pull}}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8092)
