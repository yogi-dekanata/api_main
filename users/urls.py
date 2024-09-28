from django.urls import path
from .views import TopUpView, PaymentView, TransferView, ProfileUpdateView, TransactionsReportView

urlpatterns = [
    path('topup/', TopUpView.as_view(), name='topup'),
    path('pay/', PaymentView.as_view(), name='pay'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('transactions/', TransactionsReportView.as_view(), name='transactions-report'),

]
