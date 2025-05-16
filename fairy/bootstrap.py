# -*- coding: utf-8 -*-
# cython: language_level=3
from lib import process


def main() -> None:
    # Launch the process, should run infinitely.
    proc_frontend: process.Proc = None
    proc_camera: process.Proc = None
    proc_agent: process.Proc = None
    try:
        # Launch the kernel modules.
        proc_frontend = process.launch_subprocess("frontend")
        proc_camera = process.launch_subprocess("camera")
        proc_agent = process.launch_subprocess("agent")
        # Wait for module exits.
        proc_frontend.communicate()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e
    finally:
        # Terminate all the subprocess.
        process.terminate(proc_agent)
        process.terminate(proc_camera)
        process.terminate(proc_frontend)


if __name__ == '__main__':
    main()
