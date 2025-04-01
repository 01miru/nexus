import io

import openpyxl
from process_manager.models import Snapshot
from process_manager.processes.base_process import BaseProcess


class ExportSnapshotToExcelProcess(BaseProcess):
    @staticmethod
    def process(snapshot: Snapshot) -> io.BytesIO:
        processes = snapshot.processes.all().values(
            "pid", "name", "start_time", "duration", "status", "cpu", "memory"
        )

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Snapshot Processes"

        headers = ["PID", "Name", "Start Time", "Duration", "Status", "CPU", "Memory"]
        sheet.append(headers)

        for process in processes:
            start_time = (
                process["start_time"].replace(tzinfo=None)
                if process["start_time"]
                else None
            )
            sheet.append(
                [
                    process["pid"],
                    process["name"],
                    start_time,
                    process["duration"],
                    process["status"],
                    process["cpu"],
                    process["memory"],
                ]
            )

        output = io.BytesIO()
        workbook.save(output)
        output.seek(0)

        return output
