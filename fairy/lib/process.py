# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from typing import TypeAlias
from lib import path

Proc: TypeAlias = subprocess.Popen | None


def launch(module_name: str) -> subprocess.Popen:
    return subprocess.Popen([sys.executable, os.path.join(path.PATH_KERNEL, f"{module_name}.py")])


def terminate(proc: Proc) -> None:
    if proc is None:
        return
    # Kill the process.
    proc.terminate()
