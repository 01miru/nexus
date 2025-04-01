import psutil
from django.contrib.auth.models import User
from process_manager.models import ProcessKillHistory
from process_manager.processes.base_process import BaseProcess


class KillProcessProcess(BaseProcess):
    @staticmethod
    def process(pid: int, user: User) -> bool:
        try:
            process = psutil.Process(pid)

            ProcessKillHistory.objects.create(
                process_name=process.name(),
                pid=pid,
                killed_by=user,
            )

            process.terminate()

            return True
        except psutil.NoSuchProcess:
            return False
