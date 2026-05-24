from django.urls import path
from . import views

urlpatterns = [
    path('recipients/', views.RecipientListView.as_view(), name='recipient_list'),
    path('recipients/new/', views.RecipientCreateView.as_view(), name='recipient_new'),
    path('recipients/edit/<int:pk>/', views.RecipientUpdateView.as_view(), name='recipient_edit'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/new/', views.MessageCreateView.as_view(), name='message_new'),
    path('messages/edit/<int:pk>/', views.MessageUpdateView.as_view(), name='message_edit'),
    path('mailings/', views.MailingListView.as_view(), name='mailing_list'),
    path('mailings/new/', views.MailingCreateView.as_view(), name='mailing_new'),
    path('mailings/edit/<int:pk>/', views.MailingUpdateView.as_view(), name='mailing_edit'),
    path('recipients/delete/<int:pk>/', views.RecipientDeleteView.as_view(), name='recipient_delete'),
    path('messages/delete/<int:pk>/', views.MessageDeleteView.as_view(), name='message_delete'),
    path('mailings/delete/<int:pk>/', views.MailingDeleteView.as_view(), name='mailing_delete'),
]
