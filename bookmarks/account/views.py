from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from account.forms import LoginForm


# 로그인 커스텀 인증 뷰
def user_login(request: HttpRequest):
    if request.method == "POST":
        forms = LoginForm(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                return HttpResponse("Authenticated successfully")
            else:
                return HttpResponse("Disabled account")
        else:
            return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request: HttpRequest):
    return render(request, "account/dashboard.html", {"section": "dashboard"})
