from django.urls import path, include
from django.contrib.auth import views as auth_views

from account import views

urlpatterns = [
    # path("login/", views.user_login, name="login"),
    # path(
    #     "login/",
    #     auth_views.LoginView.as_view(template_name="account/login.html"),
    #     name="login",
    # ),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # # 패스워드 URL 변경
    # path(
    #     "password-change/",
    #     auth_views.PasswordChangeView.as_view(),
    #     name="password_change",
    # ),
    # path(
    #     "password-change/done/",
    #     auth_views.PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # # 패스워드 URL 재설정
    # path(
    #     "password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    # ),
    # path(
    #     "password-reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>",
    #     auth_views.PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-reset/complete",
    #     auth_views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
    # django.contrib.auth.urls 는 위의 코드를 전부 포함한다.
    path("", include("django.contrib.auth.urls")),
    path("", views.dashboard, name="dashboard"),
]
