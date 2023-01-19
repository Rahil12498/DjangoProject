from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
  path('become-seller/', views.become_seller, name='become_seller'),
  path('seller-admin/', views.seller_admin, name='seller_admin'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('login/', auth_views.LoginView.as_view(template_name='seller/login.html'), name='login'),
  path('add-product/', views.add_product, name='add_product'),
  path('edit-seller/', views.edit_seller, name='edit_seller'),
  path('edit-product/<slug:product_slug>/', views.edit_product, name='edit_product'),
  path('', views.sellers, name='sellers'),
  path('<int:seller_id>/', views.seller, name='seller'),
]