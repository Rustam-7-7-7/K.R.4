from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Recipient, Message, Mailing
from .forms import RecipientForm, MessageForm, MailingForm

class RecipientListView(ListView):
    model = Recipient
    template_name = 'clients/recipient_list.html'
    context_object_name = 'recipients'


class MessageListView(ListView):
    model = Message
    template_name = 'clients/message_list.html'
    context_object_name = 'messages'


class MailingListView(ListView):
    model = Mailing
    template_name = 'clients/mailing_list.html'
    context_object_name = 'mailings'


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('recipient_list')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'clients/message_form.html'
    success_url = reverse_lazy('message_list')


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'clients/mailing_form.html'
    success_url = reverse_lazy('mailing_list')
