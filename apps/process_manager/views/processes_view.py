from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProcessesView(LoginRequiredMixin, TemplateView):
    template_name = "process_manager/process_list.html"
