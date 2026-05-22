from django.contrib import admin
from django.core.mail import send_mail
from django.utils import timezone
from .models import Recipient, Message, Mailing, MailingAttempt

def send_mailing(modeladmin, request, queryset):
    now = timezone.now()
    for mailing in queryset:
        if mailing.start_time <= now <= mailing.end_time and mailing.status == 'Создана':
            for recipient in mailing.recipients.all():
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email='your_email@example.com',  # Замените на ваш email
                        recipient_list=[recipient.email],
                    )
                    status = 'Успешно'
                    server_response = 'Письмо отправлено'
                except Exception as e:
                    status = 'Не успешно'
                    server_response = str(e)

                MailingAttempt.objects.create(
                    mailing=mailing,
                    recipient=recipient,
                    status=status,
                    server_response=server_response
                )

            mailing.status = 'Запущена'
            mailing.save()
    modeladmin.message_user(request, "Выбранные рассылки были отправлены.")

class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')

class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'status', 'message')
    actions = [send_mailing]

class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'recipient', 'attempt_time', 'status', 'server_response')

admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Mailing, MailingAdmin)
admin.site.register(MailingAttempt, MailingAttemptAdmin)
