from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from process_manager.models import Snapshot


class SnapshotDetailsView(LoginRequiredMixin, DetailView):
    model = Snapshot
    template_name = "process_manager/elements/_snapshot_modal_details.html"
    context_object_name = "snapshot"
    pk_url_kwarg = "snapshot_id"
