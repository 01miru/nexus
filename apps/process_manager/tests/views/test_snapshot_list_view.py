from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from process_manager.models import Snapshot


class SnapshotsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

        self.snapshot1 = Snapshot.objects.create(
            created_by=self.user, created_at=timezone.now()
        )
        self.snapshot2 = Snapshot.objects.create(
            created_by=self.user, created_at=timezone.now()
        )

    def tearDown(self):
        self.user.delete()

    def test_snapshots_list_view(self):
        response = self.client.get(reverse("process_manager:snapshots-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "process_manager/snapshots_list.html")
        self.assertIn("snapshots", response.context)
        self.assertEqual(len(response.context["snapshots"]), 2)
