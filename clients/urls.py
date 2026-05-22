from django.urls import path
from . import views

urlpatterns = [
    path('recipients/', views.RecipientListView.as_view(), name='recipient_list'),
    path('recipients/new/', views.RecipientCreateView.as_view(), name='recipient_new'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/new/', views.MessageCreateView.as_view(), name='message_new'),
    path('mailings/', views.MailingListView.as_view(), name='mailing_list'),
    path('mailings/new/', views.MailingCreateView.as_view(), name='mailing_new'),
]
