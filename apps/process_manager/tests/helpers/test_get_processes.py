import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from process_manager.helpers.get_processes import get_processes


class TestGetProcesses(unittest.TestCase):
    @patch("process_manager.helpers.get_processes.psutil.process_iter")
    def test_get_processes(self, mock_process_iter):
        mock_process = MagicMock()
        mock_process.info = {
            "pid": 1234,
            "name": "test_process",
            "username": "test_user",
            "status": "running",
            "create_time": (datetime.now() - timedelta(hours=1)).timestamp(),
            "cpu_percent": 10.0,
            "memory_info": MagicMock(rss=1024 * 1024 * 100),
        }
        mock_process.memory_info.return_value = MagicMock(rss=1024 * 1024 * 100)
        mock_process_iter.return_value = [mock_process]

        processes = get_processes()

        self.assertEqual(len(processes), 1)
        self.assertEqual(processes[0]["pid"], 1234)
        self.assertEqual(processes[0]["name"], "test_process")
        self.assertEqual(processes[0]["username"], "test_user")
        self.assertEqual(processes[0]["status"], "running")
        self.assertEqual(processes[0]["cpu_usage"], 10.0)
        self.assertEqual(processes[0]["memory_usage"], 100.0)
        self.assertTrue("duration" in processes[0])

    @patch("process_manager.helpers.get_processes.psutil.process_iter")
    def test_should_return_zero_results_due_to_excluded_pid(self, mock_process_iter):
        mock_process = MagicMock()
        mock_process.info = {
            "pid": 0,
            "name": "test_process",
            "username": "test_user",
            "status": "running",
            "create_time": (datetime.now() - timedelta(hours=1)).timestamp(),
            "cpu_percent": 10.0,
            "memory_info": MagicMock(rss=1024 * 1024 * 100),
        }
        mock_process_iter.return_value = [mock_process]

        processes = get_processes()

        self.assertEqual(len(processes), 0)
