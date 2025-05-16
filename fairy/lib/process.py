# -*- coding: utf-8 -*-
# cython: language_level=3
import os
import sys
import platform
import subprocess
from typing import TypeAlias
from lib import path

Proc: TypeAlias = subprocess.Popen | None


def __run_python(*args) -> subprocess.Popen:
    return subprocess.Popen([sys.executable, *args], cwd=os.getcwd())


def launch_subprocess(module_name: str) -> subprocess.Popen:
    def __run_as_module():
        return __run_python("-c", f"import importlib;mod=importlib.import_module('kernel.{module_name}');mod.main()")

    # On Windows, it is probably named as .pyd file.
    if platform.system() == "Windows":
        # Check .pyd file first.
        pyd_path: str = os.path.join(path.PATH_KERNEL, f"{module_name}.pyd")
        if os.path.isfile(pyd_path):
            # Run as module.
            return __run_as_module()
    # On Linux, it is probably named as .so file.
    if platform.system() == "Linux":
        # Check .so file first.
        so_path: str = os.path.join(path.PATH_KERNEL, f"{module_name}.so")
        if os.path.isfile(so_path):
            return __run_as_module()
    # Check whether the py module exist.
    py_path: str = os.path.join(path.PATH_KERNEL, f"{module_name}.py")
    if os.path.isfile(py_path):
        return __run_python(os.path.join(path.PATH_KERNEL, f"{module_name}.py"))
    # Failed to find the process.
    raise FileNotFoundError(f"no kernel module {module_name} found")


def terminate(proc: Proc) -> None:
    if proc is None:
        return
    # Kill the process.
    proc.terminate()
