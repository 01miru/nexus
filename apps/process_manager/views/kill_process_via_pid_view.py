from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic.base import View
from process_manager.processes import KillProcessProcess


class KillProcessViaPidView(LoginRequiredMixin, View):
    kill_process: KillProcessProcess | None = None

    def get(self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        self.kill_process.process(  # type: ignore[union-attr]
            cast(int, kwargs.get("pid")), user=cast(User, request.user)
        )

        return HttpResponse("")
