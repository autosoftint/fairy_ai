# -*- coding: utf-8 -*-
from lib import process


def main() -> None:
    # Launch the processes, should run infinitely.
    proc_frontend: process.Proc = None
    proc_sensor: process.Proc = None
    proc_agent: process.Proc = None
    try:
        # Launch the kernel modules.
        proc_frontend = process.launch_subprocess("frontend")
        proc_sensor = process.launch_subprocess("sensor")
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
        process.terminate(proc_sensor)
        process.terminate(proc_frontend)


if __name__ == '__main__':
    main()
