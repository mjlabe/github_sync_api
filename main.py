import os
import subprocess
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Request, Header

from verify_signature import verify_signature


app = FastAPI()


@app.post("/pull")
async def pull_changes(request: Request, x_hub_signature_256: Annotated[str | None, Header()]):
    # verify request comes from GitHub webhook
    await verify_signature(request)

    fetch = subprocess.run(["git", "fetch"], cwd=os.environ.get("REPO_PATH"), capture_output=True, text=True)
    pull = subprocess.run(["git", "pull"], cwd=os.environ.get("REPO_PATH"), capture_output=True, text=True)

    return {"message": {"fetch": fetch, "pull": pull}}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8092)
