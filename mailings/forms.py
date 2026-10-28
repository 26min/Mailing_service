from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "recipients"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "message": forms.Select(attrs={"class": "form-control"}),
            "recipients": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and start_time < timezone.now():
            raise forms.ValidationError("Дата начала не может быть в прошлом.")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(
                "Дата начала должна быть раньше даты окончания."
            )

        return cleaned_data


User = get_user_model()


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(
#         required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
#     )
#
#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")
#
#
# User = get_user_model()


class RegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""

    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
