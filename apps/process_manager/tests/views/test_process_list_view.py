from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class ProcessesListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    @patch("process_manager.views.processes_list_view.get_processes")
    def test_processes_list_view(self, mock_get_processes):
        mock_process = {
            "pid": 1234,
            "name": "test_process",
            "username": "test_user",
            "status": "running",
            "create_time": "2023-01-01 00:00:00",
            "duration": "1d 2h 30m",
            "cpu_usage": 10.0,
            "memory_usage": 100.0,
            "memory_info": MagicMock(rss=1024 * 1024 * 100),
        }
        mock_get_processes.return_value = [mock_process]

        response = self.client.get(reverse("process_manager:processes-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "process_manager/elements/_process_row.html")
        self.assertIn("processes", response.context)
        self.assertEqual(len(response.context["processes"]), 1)
        self.assertEqual(response.context["processes"][0]["pid"], 1234)
