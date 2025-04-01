from django.urls import path

from .processes import (
    ExportSnapshotToExcelProcess,
    KillProcessProcess,
    TakeSnapshotProcess,
)
from .views import (
    KilledProcessesView,
    KillProcessViaPidView,
    ProcessesView,
    SnapshotDetailsView,
    SnapshotExportView,
    SnapshotsListView,
    TakeSnapshotView,
)
from .views.processes_list_view import ProcessesListView

app_name = "process_manager"

urlpatterns = [
    path("processes/", ProcessesView.as_view(), name="processes"),
    path("processes-list/", ProcessesListView.as_view(), name="processes-list"),
    path(
        "processes/kill/<int:pid>/",
        KillProcessViaPidView.as_view(kill_process=KillProcessProcess()),
        name="kill-process",
    ),
    path(
        "processes/kill/list/",
        KilledProcessesView.as_view(),
        name="kill-processes-list",
    ),
    path(
        "processes/take-snapshot/",
        TakeSnapshotView.as_view(take_snapshot_process=TakeSnapshotProcess()),
        name="take-snapshot",
    ),
    path("processes/snapshots/", SnapshotsListView.as_view(), name="snapshots-list"),
    path(
        "processes/snapshots/<int:snapshot_id>/",
        SnapshotDetailsView.as_view(),
        name="snapshot-detail",
    ),
    path(
        "processes/snapshots/<int:snapshot_id>/export/",
        SnapshotExportView.as_view(
            export_snapshot_to_excel_process=ExportSnapshotToExcelProcess()
        ),
        name="snapshot-detail-export",
    ),
]
