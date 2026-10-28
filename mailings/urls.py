from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "mailings"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # Recipient
    path("recipients/", views.RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipients/create/",
        views.RecipientCreateView.as_view(),
        name="recipient_create",
    ),
    path(
        "recipients/<int:pk>/update/",
        views.RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipients/<int:pk>/delete/",
        views.RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    # Message
    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/update/",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "messages/<int:pk>/delete/",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    # Mailing
    path("mailings/", views.MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailings/<int:pk>/update/",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailings/<int:pk>/delete/",
        views.MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path(
        "mailings/<int:pk>/send/", views.MailingSendView.as_view(), name="mailing_send"
    ),
    # Аутентификация
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="mailings/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="mailings/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="mailings/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="mailings/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="mailings/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("register/", views.RegisterView.as_view(), name="register"),
]
