# -*- coding: utf-8 -*-
# cython: language_level=3
import uvicorn
from fastapi import FastAPI
from lib.version import VERSION
import config

app = FastAPI(title="Fairy Localhost Server",
              version=VERSION,)


def main() -> None:
    print("starting frontend server...")
    uvicorn.run(app, host="127.0.0.1", port=config.FRONTEND_PORT,
                log_level=config.FRONTEND_LOG)


if __name__ == "__main__":
    main()
