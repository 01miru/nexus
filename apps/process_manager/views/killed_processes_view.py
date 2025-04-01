from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from process_manager.models import ProcessKillHistory


class KilledProcessesView(LoginRequiredMixin, ListView):
    template_name: str = "process_manager/killed_processes_list.html"
    context_object_name = "processes"
    model = ProcessKillHistory
