from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Recipient, Message, Mailing
from .forms import RecipientForm, MessageForm, MailingForm

class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'clients/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(user=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'clients/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists():
            return Message.objects.all()
        return Message.objects.filter(user=self.request.user)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'clients/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)

#
# class MailingListView(LoginRequiredMixin, ListView):
#     model = Mailing
#     template_name = 'clients/mailing_list.html'
#     context_object_name = 'mailings'
#
#     @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def get_queryset(self):
#         return Mailing.objects.filter(user=self.request.user)




class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('recipient_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'clients/message_form.html'
    success_url = reverse_lazy('message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'clients/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('recipient_list')

    def test_func(self):
        # Логика для проверки, может ли пользователь редактировать получателя
        return True  # Измени на логику проверки


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'clients/message_form.html'
    success_url = reverse_lazy('message_list')

    def test_func(self):
        # Логика для проверки, может ли пользователь редактировать сообщение
        return True  # Измени на логику проверки


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'clients/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def test_func(self):
        # Логика для проверки, может ли пользователь редактировать рассылку
        return True  # Измени на логику проверки


class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipient
    template_name = 'clients/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')

    def test_func(self):
        # Логика для проверки, может ли пользователь удалить получателя
        return True  # Измени на логику проверки


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'clients/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

    def test_func(self):
        # Логика для проверки, может ли пользователь удалить сообщение
        return True  # Измени на логику проверки


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = 'clients/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')

    def test_func(self):
        # Логика для проверки, может ли пользователь удалить рассылку
        return True  # Измени на логику проверки




from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'clients/register.html', {'form': form})



from django.views.generic import TemplateView
from django.db.models import Count, Q
from .models import Mailing, MailingAttempt

class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'clients/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Общая статистика по рассылкам
        context['total_mailings'] = Mailing.objects.filter(user=self.request.user).count()
        context['active_mailings'] = Mailing.objects.filter(user=self.request.user, status='Запущена').count()

        # Статистика по попыткам
        context['total_attempts'] = MailingAttempt.objects.filter(mailing__user=self.request.user).count()
        context['successful_attempts'] = MailingAttempt.objects.filter(
            mailing__user=self.request.user, status='Успешно').count()
        context['unsuccessful_attempts'] = MailingAttempt.objects.filter(
            mailing__user=self.request.user, status='Не успешно').count()

        return context
