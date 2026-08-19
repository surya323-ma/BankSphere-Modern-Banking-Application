from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('transactions/<str:txn_id>/', views.transaction_detail_view, name='transaction_detail'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]
