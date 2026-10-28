from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipient(models.Model):
    """Получатель рассылки (клиент)"""

    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=150, verbose_name="Ф. И. О.")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="recipients",
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    """Сообщение для рассылки"""

    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="messages"
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    """Рассылка"""

    STATUS_CHOICES = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Создана", verbose_name="Статус"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="mailings"
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Рассылка {self.id} ({self.message.subject})"


class Attempt(models.Model):
    """Попытка отправки"""

    STATUS_CHOICES = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]

    attempt_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    server_response = models.TextField(verbose_name="Ответ сервера")
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="attempts",
    )

    class Meta:
        verbose_name = "Попытка отправки"
        verbose_name_plural = "Попытки отправки"

    def __str__(self):
        return f"Попытка {self.id} — {self.status}"
