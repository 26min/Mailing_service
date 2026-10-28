from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import MailingForm, MessageForm, RecipientForm, RegisterForm
from .models import Attempt, Mailing, Message, Recipient
from .services import send_mailing

# ГЛАВНАЯ СТРАНИЦА


@method_decorator(cache_page(60 * 5), name="dispatch")
class HomeView(TemplateView):
    """Главная страница со статистикой"""

    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        if self.request.user.is_superuser:
            mailings = Mailing.objects.all()
            recipients = Recipient.objects.all()
            attempts = Attempt.objects.all()
        else:
            mailings = Mailing.objects.filter(owner=self.request.user)
            recipients = Recipient.objects.filter(owner=self.request.user)
            attempts = Attempt.objects.filter(mailing__owner=self.request.user)

        context["total_mailings"] = mailings.count()
        context["active_mailings"] = mailings.filter(
            start_time__lte=now, end_time__gte=now
        ).count()
        context["total_recipients"] = recipients.count()

        # Статистика попыток
        context["successful_attempts"] = attempts.filter(status="Успешно").count()
        context["failed_attempts"] = attempts.filter(status="Не успешно").count()
        context["total_attempts"] = attempts.count()

        return context


# RECIPIENTS


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mailings/recipient_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Managers").exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Managers").exists():
            return redirect("mailings:recipient_list")
        return super().dispatch(request, *args, **kwargs)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailings/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Managers").exists():
            return redirect("mailings:recipient_list")
        return super().dispatch(request, *args, **kwargs)


# MESSAGES


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Managers").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Managers").exists():
            return redirect("mailings:message_list")
        return super().dispatch(request, *args, **kwargs)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Managers").exists():
            return redirect("mailings:message_list")
        return super().dispatch(request, *args, **kwargs)


# MAILINGS


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Managers").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Managers").exists():
            return redirect("mailings:mailing_list")
        return super().dispatch(request, *args, **kwargs)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Managers").exists():
            return redirect("mailings:mailing_list")
        return super().dispatch(request, *args, **kwargs)


class MailingSendView(LoginRequiredMixin, TemplateView):
    """Запуск рассылки по требованию"""

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        result = send_mailing(mailing.id)

        if result["success"]:
            messages.success(request, result["message"])
        else:
            messages.error(request, result["message"])

        return redirect("mailings:mailing_list")


class RegisterView(CreateView):
    """Регистрация пользователя"""

    form_class = RegisterForm
    template_name = "mailings/register.html"
    success_url = reverse_lazy("login")
