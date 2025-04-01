from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from process_manager.models import Snapshot


class SnapshotsListView(LoginRequiredMixin, ListView):
    model = Snapshot
    template_name = "process_manager/snapshots_list.html"
    context_object_name = "snapshots"

    def get_context_data(
        self, *, object_list: Any = None, **kwargs: Any
    ) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        snapshots = Snapshot.objects.all().order_by("created_at")
        labels = [
            snapshot.created_at.strftime("%d-%m-%Y %H:%M:%S") for snapshot in snapshots
        ]
        cpu_data = [snapshot.get_total_cpu for snapshot in snapshots]
        memory_data = [snapshot.get_total_memory for snapshot in snapshots]
        processes_data = [snapshot.get_processes_count for snapshot in snapshots]

        context.update(
            {
                "labels": labels,
                "cpu_data": cpu_data,
                "memory_data": memory_data,
                "processes_data": processes_data,
            }
        )

        return context
