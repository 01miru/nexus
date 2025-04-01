from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView
from process_manager.models import Snapshot
from process_manager.processes.export_snapshot_to_excel_process import (
    ExportSnapshotToExcelProcess,
)


class SnapshotExportView(LoginRequiredMixin, DetailView):
    export_snapshot_to_excel_process: ExportSnapshotToExcelProcess | None = None
    model = Snapshot
    pk_url_kwarg = "snapshot_id"

    def get(
        self, request: HttpRequest, *args: list[Any], **kwargs: dict[str, Any]
    ) -> HttpResponse:
        response = HttpResponse(
            self.export_snapshot_to_excel_process.process(self.get_object()),  # type: ignore[union-attr]
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = (
            'attachment; filename="snapshot_processes.xlsx"'
        )

        return response
