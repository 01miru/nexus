from datetime import datetime

import psutil
from django.conf import settings

from .format_timedelta import format_timedelta


def get_processes() -> list[dict]:
    processes = psutil.process_iter(
        [
            "pid",
            "name",
            "username",
            "status",
            "create_time",
            "cpu_percent",
            "memory_info",
        ]
    )

    results = []

    for process in processes:
        try:
            process_info = process.info
            pid = process_info["pid"]

            if pid in settings.EXCLUDE_PIDS:
                continue

            create_time = datetime.fromtimestamp(process_info["create_time"])
            current_time = datetime.now()
            duration = format_timedelta(current_time - create_time)
            memory_usage = round(process.memory_info().rss / (1024 * 1024), 2)

            results.append(
                {
                    "pid": pid,
                    "name": process_info["name"],
                    "username": process_info["username"],
                    "status": process_info["status"],
                    "create_time": create_time,
                    "duration": duration,
                    "cpu_usage": process_info["cpu_percent"],
                    "memory_usage": memory_usage,
                }
            )

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return results
