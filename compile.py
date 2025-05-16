# -*- coding: utf-8 -*-
import os
import shutil
import platform
from Cython.Build.Dependencies import create_extension_list
from Cython.Build import cythonize
from distutils.command.build_ext import build_ext
from distutils import sysconfig
from setuptools import setup, Extension

PATH_BUILD: str = os.path.dirname(__file__)
PATH_SOURCE: str = os.path.join(PATH_BUILD, "fairy")

EXCEPTIONS: list = [
    "bootstrap.py"
]


class CustomBuildExt(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        suffix = sysconfig.get_config_var('EXT_SUFFIX')
        ext = os.path.splitext(filename)[1]
        # Get the directory containing the original .py file
        return filename.replace(suffix, '') + ext


def compile_py(py_dir: str, py_name: str):
    # Get the base name.
    py_basename: str = py_name[:-3]
    # Calculate the pyd name.
    if platform.system() == "Windows":
        binary_name: str = f"{py_basename}.pyd"
    elif platform.system() == "Linux":
        binary_name: str = f"{py_basename}.so"
    else:
        raise NotImplementedError(f"Unsupported platform {platform.system()}, please use the .py file")
    c_name: str = f"{py_basename}.c"
    # Calculate the py path.
    py_path: str = os.path.join(py_dir, py_name)
    c_path: str = os.path.join(py_dir, c_name)
    binary_path: str = os.path.join(PATH_BUILD, binary_name)
    # Run the program.
    setup(
        cmdclass={'build_ext': CustomBuildExt},
        ext_modules=cythonize(
            [Extension(
                "*",
                [py_path],
                extra_compile_args=["-O2"],  # Optimization flags
            )],
            compiler_directives={
                'language_level': "3",
            },
        )
    )
    # After program is completed, remove the py file and c file.
    os.remove(c_path)
    os.remove(py_path)
    # Move the pyd file to original py file location.
    shutil.move(binary_path, py_dir)


def main():
    # Ensure the source directory exist.
    if not os.path.isdir(PATH_SOURCE):
        raise NotADirectoryError(f"{PATH_SOURCE} is not a directory")
    # Walk into the source code directory, compile all the py to pyd.
    for root, dirs, files in os.walk(PATH_SOURCE):
        # Skip hidden and cache directories
        if os.path.basename(root).startswith(('.', '__')):
            continue

        for filename in files:
            if not filename.endswith(".py") or filename in EXCEPTIONS:
                continue
            # Compile the py file to pyc.
            compile_py(root, filename)


if __name__ == "__main__":
    main()
