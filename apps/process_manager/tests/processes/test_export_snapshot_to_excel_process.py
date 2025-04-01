import io
from unittest.mock import ANY

import openpyxl
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from process_manager.models import Snapshot, SnapshotProcess
from process_manager.processes.export_snapshot_to_excel_process import (
    ExportSnapshotToExcelProcess,
)


class ExportSnapshotToExcelProcessTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.snapshot = Snapshot.objects.create(
            created_by=self.user, created_at=timezone.now()
        )

        SnapshotProcess.objects.create(
            snapshot=self.snapshot,
            pid=1234,
            name="Process1",
            start_time=timezone.now(),
            duration="00:01:00",
            status="Running",
            cpu=10.5,
            memory=256.0,
        )
        SnapshotProcess.objects.create(
            snapshot=self.snapshot,
            pid=5678,
            name="Process2",
            start_time=timezone.now(),
            duration="00:02:00",
            status="Stopped",
            cpu=20.0,
            memory=512.0,
        )

    def tearDown(self):
        self.user.delete()

    def test_export_snapshot_to_excel_process(self):
        output = ExportSnapshotToExcelProcess.process(self.snapshot)
        self.assertIsInstance(output, io.BytesIO)

        workbook = openpyxl.load_workbook(output)
        sheet = workbook.active

        headers = ["PID", "Name", "Start Time", "Duration", "Status", "CPU", "Memory"]
        self.assertEqual([cell.value for cell in sheet[1]], headers)

        rows = list(sheet.iter_rows(min_row=2, max_row=3, values_only=True))
        self.assertEqual(
            rows[0],
            (
                1234,
                "Process1",
                ANY,
                "00:01:00",
                "Running",
                10.5,
                256.0,
            ),
        )
        self.assertEqual(
            rows[1],
            (
                5678,
                "Process2",
                ANY,
                "00:02:00",
                "Stopped",
                20.0,
                512.0,
            ),
        )
