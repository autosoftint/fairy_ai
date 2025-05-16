# -*- coding: utf-8 -*-
from lib import process


def main() -> None:
    # Launch the process, should run infinitely.
    proc_frontend: process.Proc = None
    try:
        # Launch the kernel modules.
        proc_frontend = process.launch("frontend")
        # Wait for module exits.
        proc_frontend.communicate()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e
    finally:
        # Terminate all the subprocess.
        process.terminate(proc_frontend)


if __name__ == '__main__':
    main()
