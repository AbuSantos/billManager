from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('add-bill/', views.add_bill, name='add_bill'),
    path('edit-bill/<int:bill_id>/', views.edit_bill, name='edit_bill'),
    path('delete-bill/<int:bill_id>/', views.delete_bill, name='delete_bill'),
    path('search-bills/', views.search_bills, name='search_bills'),
    path('send-test-email/', views.send_test_email, name='send_test_email'),

]
