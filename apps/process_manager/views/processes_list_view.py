from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from process_manager.helpers.get_processes import get_processes


class ProcessesListView(LoginRequiredMixin, TemplateView):
    template_name: str = "process_manager/elements/_process_row.html"

    def get_context_data(self, **kwargs: Any) -> dict:
        ctx = super().get_context_data(**kwargs)
        ctx["processes"] = get_processes()

        return ctx
