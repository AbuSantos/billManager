from django.urls import path,include
from django.conf.urls import handler404, handler500
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('add-bill/', views.add_bill, name='add_bill'),
    path('edit-bill/<int:bill_id>/', views.edit_bill, name='edit_bill'),
    path('delete-bill/<int:bill_id>/', views.delete_bill, name='delete_bill'),
    path('search-bills/', views.search_bills, name='search_bills'),
    path('send-test-email/', views.send_test_email, name='send_test_email'),
    path('wallet', views.wallet, name='wallet'),
    path('deposit/', views.deposit, name='deposit'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('bill-payments/', views.bill_payments, name='bill_payments')
]
