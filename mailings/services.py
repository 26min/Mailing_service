from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Attempt, Mailing


def send_mailing(mailing_id):
    """
    Отправляет рассылку по ID.
    Возвращает словарь с результатом:
    {'success': bool, 'message': str, 'sent': int, 'failed': int}
    """
    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        return {
            "success": False,
            "message": "Рассылка не найдена",
            "sent": 0,
            "failed": 0,
        }

    now = timezone.now()

    # 1. Проверяем время
    if not (mailing.start_time <= now <= mailing.end_time):
        return {
            "success": False,
            "message": f"Сейчас нельзя отправить рассылку. Она активна с {mailing.start_time} по {mailing.end_time}",
            "sent": 0,
            "failed": 0,
        }

    # 2. Получаем реципиентов
    recipients = mailing.recipients.all()

    if not recipients:
        return {"success": False, "message": "Нет получателей", "sent": 0, "failed": 0}

    # 3. Готовим попытки
    attempts_to_create = []
    sent_count = 0
    failed_count = 0

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            attempts_to_create.append(
                Attempt(mailing=mailing, status="Успешно", server_response="OK")
            )
            sent_count += 1
        except Exception as e:
            attempts_to_create.append(
                Attempt(mailing=mailing, status="Не успешно", server_response=str(e))
            )
            failed_count += 1

    # 4. Сохраняем все попытки одним запросом
    if attempts_to_create:
        Attempt.objects.bulk_create(attempts_to_create)

    # 5. Меняем статус рассылки
    mailing.status = "Запущена"
    mailing.save()

    return {
        "success": True,
        "message": f"Отправлено: {sent_count}, ошибок: {failed_count}",
        "sent": sent_count,
        "failed": failed_count,
    }
