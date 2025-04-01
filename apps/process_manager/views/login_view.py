from typing import Any

from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name: str = "process_manager/login.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("process_manager:processes")

        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        username: str = request.POST.get("username", "")
        password: str = request.POST.get("password", "")
        remember_me: bool = bool(request.POST.get("remember_me", False))

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)

            return HttpResponse("OK")
        else:
            return HttpResponseForbidden("Wrong authentication data")
