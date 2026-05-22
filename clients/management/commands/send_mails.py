from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from clients.models import Mailing

class Command(BaseCommand):
    help = 'Send out email campaigns'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        mailings = Mailing.objects.filter(start_time__lte=now, end_time__gte=now, status='Создана')

        for mailing in mailings:
            for recipient in mailing.recipients.all():
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email='your_email@example.com',  # Замените на ваш email
                    recipient_list=[recipient.email],
                )
            mailing.status = 'Запущена'
            mailing.save()

        self.stdout.write(self.style.SUCCESS('Emails sent successfully!'))
