from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from process_manager.models import ProcessKillHistory


class KilledProcessesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.url = reverse("process_manager:kill-processes-list")

        ProcessKillHistory.objects.create(
            kill_time="2023-10-01T12:00:00Z",
            killed_by=cls.user,
            process_name="test_process_1",
            pid=123,
        )
        ProcessKillHistory.objects.create(
            kill_time="2023-10-01T12:05:00Z",
            killed_by=cls.user,
            process_name="test_process_2",
            pid=124,
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="12345")

    def test_killed_processes_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_killed_processes_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "process_manager/killed_processes_list.html")

    def test_killed_processes_view_context(self):
        response = self.client.get(self.url)
        self.assertIn("processes", response.context)
        self.assertEqual(len(response.context["processes"]), 2)
