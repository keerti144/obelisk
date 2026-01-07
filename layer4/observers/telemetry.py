import psutil
import time

def sample_cpu(proc, duration=2):
    try:
        p = psutil.Process(proc.pid)
        samples = []
        for _ in range(duration):
            samples.append(p.cpu_percent(interval=1))
        avg = sum(samples) / len(samples)

        if avg < 10:
            pressure = "low"
        elif avg < 50:
            pressure = "medium"
        else:
            pressure = "high"

        return {"cpu_pressure": pressure}
    except Exception:
        return {"cpu_pressure": "unknown"}
