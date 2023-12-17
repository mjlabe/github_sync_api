import os

import uvicorn
from fastapi import FastAPI

from github import Github

from github import Auth

app = FastAPI()


def get_repos():
    # using an access token
    auth = Auth.Token(os.environ.get("access_token"))
    g = Github(auth=auth)

    ro = []
    for repo in g.get_user().get_repos():
        ro.append(repo.name)

    # To close connections after use
    g.close()

    return ro


def get_repo(repo: str):
    # using an access token
    auth = Auth.Token(os.environ.get("access_token"))
    g = Github(auth=auth)
    user = g.get_user().login

    repo = g.get_repo(f"{user}/{repo}")

    # To close connections after use
    g.close()

    return repo


@app.get("/repo")
async def get_repo_list():
    print("GET")
    repos = get_repos()
    return {"repos": repos}


@app.get("/repo/{repo}")
async def sync_info(repo: str):
    print("GET")
    repo = get_repo(repo=repo)
    return {"repo": repo.name}


@app.post("/sync")
async def sync(branch: str):
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
