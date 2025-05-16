# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI
from lib.version import VERSION

app = FastAPI(title="Fairy Localhost Server",
              version=VERSION,)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
