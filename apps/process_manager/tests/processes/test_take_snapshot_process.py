import unittest

from django.contrib.auth.models import User
from process_manager.models import Snapshot, SnapshotProcess
from process_manager.processes.take_snapshot_process import TakeSnapshotProcess


class TestTakeSnapshotProcess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_take_snapshot_process(self):
        processes = [
            {
                "pid": 1234,
                "name": "test_process_1",
                "create_time": "2023-10-01T12:00:00Z",
                "duration": "00:01:00",
                "status": "running",
                "cpu_usage": 10.5,
                "memory_usage": 256.0,
            },
            {
                "pid": 5678,
                "name": "test_process_2",
                "create_time": "2023-10-01T12:05:00Z",
                "duration": "00:02:00",
                "status": "sleeping",
                "cpu_usage": 5.0,
                "memory_usage": 128.0,
            },
        ]

        TakeSnapshotProcess.process(processes=processes, created_by=self.user)

        snapshot = Snapshot.objects.get(created_by=self.user)

        self.assertIsNotNone(snapshot)

        snapshot_processes = SnapshotProcess.objects.filter(snapshot=snapshot)

        self.assertEqual(snapshot_processes.count(), 2)

        for process in processes:
            self.assertTrue(
                snapshot_processes.filter(
                    pid=process["pid"],
                    name=process["name"],
                    start_time=process["create_time"],
                    duration=process["duration"],
                    status=process["status"],
                    cpu=process["cpu_usage"],
                    memory=process["memory_usage"],
                ).exists()
            )


if __name__ == "__main__":
    unittest.main()
