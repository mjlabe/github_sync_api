import os
import subprocess

import logging

import uvicorn
from fastapi import FastAPI, Request, HTTPException

from settings import settings
from verify_remotes import verify


app = FastAPI()


@app.post("/clone")
@verify
async def pull_changes(request: Request, repo_url: str, local_path: str):
    logging.info(f"Client {request.client.host} requested cloning repo '{repo_url}'")
    rm = subprocess.run(
        ["rm", "-R", local_path], cwd=local_path, capture_output=True, text=True
    )
    clone = subprocess.run(
        ["git", "clone", repo_url], cwd=local_path, capture_output=True, text=True
    )
    logging.info(str({"message": {"rm": rm, "clone": clone}}))
    return {"message": {"clone": clone}}


@app.post("/{repo}/checkout")
@verify
async def pull_changes(request: Request, repo: str, branch: str):
    repo = settings["repos"].get(repo)

    logging.info(f"Client {request.client.host} requested checking out branch {branch} for repo '{repo}'")

    fetch = subprocess.run(
        ["git", "fetch"], cwd=repo, capture_output=True, text=True
    )

    checkout = subprocess.run(
        ["git", "switch", branch], cwd=repo, capture_output=True, text=True
    )

    logging.info(str({"message": {"fetch": fetch, "checkout": checkout, }}))
    return {"message": {"fetch": fetch, "checkout": checkout, }}


@app.post("/{repo}/pull")
@verify
async def pull_changes(request: Request, repo: str):
    logging.info(f"Client {request.client.host} requested pulling changes for repo '{repo}'")

    repo = settings["repos"].get(repo)

    if not repo:
        logging.warning(f"Repo {repo} is not defined in settings")
        raise HTTPException(detail="Repo is not defined in settings", status_code=404)

    pre_run = None
    if pre_script := settings.get("scripts", {}).get("pre_run"):
        pre_run = subprocess.run(
            [pre_script], cwd=repo, capture_output=True, text=True
        )

    fetch = subprocess.run(
        ["git", "fetch"], cwd=repo, capture_output=True, text=True
    )
    pull = subprocess.run(
        ["git", "pull"], cwd=repo, capture_output=True, text=True
    )

    post_run = None
    if post_script := settings.get("scripts", {}).get("post_run"):
        post_run = subprocess.run(
            [post_script], cwd=repo, capture_output=True, text=True
        )

    logging.info(str({"message": {"pre-run": pre_run, "fetch": fetch, "pull": pull, "post_run": post_run}}))
    return {"message": {"pre-run": pre_run, "fetch": fetch, "pull": pull, "post_run": post_run}}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8092)
