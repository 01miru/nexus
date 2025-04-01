from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.views import View
from process_manager.helpers.get_processes import get_processes
from process_manager.processes.take_snapshot_process import TakeSnapshotProcess


class TakeSnapshotView(LoginRequiredMixin, View):
    take_snapshot_process: TakeSnapshotProcess | None = None

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> JsonResponse:
        self.take_snapshot_process.process(  # type: ignore[union-attr]
            processes=get_processes(), created_by=cast(User, request.user)
        )

        return JsonResponse(
            {"status": "success", "message": "Snapshot taken successfully"}
        )
