# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

from setuptools import setup
from Cython.Build import cythonize

PATH_ROOT: str = os.path.dirname(__file__)
PATH_BUILD: str = os.path.join(PATH_ROOT, "__build")
PATH_FAIRY: str = os.path.join(PATH_ROOT, "fairy")


def prepare_workdir():
    # Reset the build directory.
    if os.path.isdir(PATH_BUILD):
        shutil.rmtree(PATH_BUILD)
    if not os.path.isdir(PATH_BUILD):
        os.makedirs(PATH_BUILD, exist_ok=True)
    # Copy the entire source directory to build directory.
    path_target_fairy: str = os.path.join(PATH_BUILD, "fairy")
    shutil.copytree(PATH_FAIRY, path_target_fairy)


def main():
    # Prepare the working directory.
    prepare_workdir()
    # Copy the compile.py and pyproject.toml to build directory.
    shutil.copyfile(os.path.join(PATH_ROOT, "compile.py"), os.path.join(PATH_BUILD, "compile.py"))
    shutil.copyfile(os.path.join(PATH_ROOT, "pyproject.toml"), os.path.join(PATH_BUILD, "pyproject.toml"))
    # Run the compile.py.
    proc = subprocess.Popen([sys.executable, "compile.py", "build_ext", "--inplace"], cwd=PATH_BUILD)
    proc.communicate()


if __name__ == "__main__":
    main()
