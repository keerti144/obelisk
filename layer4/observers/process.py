import time

def observe_process(proc, timeout=10):
    start = time.time()

    try:
        proc.wait(timeout=timeout)
        exited = True
    except Exception:
        exited = False

    runtime = time.time() - start

    return {
        "process_started": True,
        "process_exited": exited,
        "exit_code": proc.poll(),
        "runtime_seconds": round(runtime, 2)
    }
