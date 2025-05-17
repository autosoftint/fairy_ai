# -*- coding: utf-8 -*-
# cython: language_level=3
import os
import uvicorn
import aiofiles
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from lib.version import VERSION
from lib import path
import config

app = FastAPI(title="Fairy Localhost Server",
              version=VERSION,)
# Mount the static file from the web directory.
app.mount("/static", StaticFiles(directory=path.PATH_WEB_STATIC), name="static")
# Construct the homepage path.
path_homepage: str = os.path.join(path.PATH_WEB, "index.html")
# Prepare the homepage cache.
homepage_modified: float | None = None
homepage_cache: str = ""


@app.get("/", response_class=HTMLResponse)
async def homepage():
    # This serve the index.html for the root path, check file existence.
    if os.path.isfile(path_homepage):
        global homepage_cache
        # Check whether the homepage is loaded.
        current_timestamp: float = os.path.getmtime(path_homepage)
        if homepage_modified is None or current_timestamp > homepage_modified:
            # Need to update the homepage cache.
            async with aiofiles.open(path_homepage, "r", encoding="utf-8") as homepage_file:
                homepage_cache = await homepage_file.read()
        # Provide the content as HTMLResponse.
        return HTMLResponse(homepage_cache)
    raise HTTPException(status_code=404)


def main() -> None:
    print("starting frontend server...", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=config.FRONTEND_PORT,
                log_level=config.FRONTEND_LOG)


if __name__ == "__main__":
    main()
