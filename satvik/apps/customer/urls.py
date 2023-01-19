from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  path('signup/', views.signup, name='signup'),
  path('customer-account/', views.customer_account, name='customer_account'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('login/', auth_views.LoginView.as_view(template_name='customer/login.html'), name='login'),
  path('edit_customer/', views.edit_customer, name='edit_customer'),
  path('delete_order/<int:order_id>', views.delete_order, name='delete_order'),
]
