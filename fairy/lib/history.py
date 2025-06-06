# -*- coding: utf-8 -*-
# cython: language_level=3
import os
import json
import aiofiles
from lib.path import PATH_STORAGE

PATH_RECORD: str = os.path.join(PATH_STORAGE, "records.json")


async def load_records() -> dict:
    if not os.path.isfile(PATH_RECORD):
        return {}
    # Load the record data from the disk.
    try:
        async with aiofiles.open(PATH_RECORD) as record_file:
            return json.loads(await record_file.read())
    except Exception as e:
        print(f"Error happens when loading records: {e}")
        return {}


async def save_records(records: dict) -> None:
    pass
