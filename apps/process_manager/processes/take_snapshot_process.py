from django.contrib.auth.models import User
from django.db import transaction
from process_manager.models import Snapshot, SnapshotProcess
from process_manager.processes.base_process import BaseProcess


class TakeSnapshotProcess(BaseProcess):
    @staticmethod
    @transaction.atomic
    def process(processes: list[dict], created_by: User) -> None:
        snapshot = Snapshot.objects.create(created_by=created_by)

        snapshot_processes = [
            SnapshotProcess(
                snapshot=snapshot,
                pid=process["pid"],
                name=process["name"],
                start_time=process["create_time"],
                duration=process["duration"],
                status=process["status"],
                cpu=process["cpu_usage"],
                memory=process["memory_usage"],
            )
            for process in processes
        ]

        SnapshotProcess.objects.bulk_create(snapshot_processes)
