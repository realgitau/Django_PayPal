from django.urls import path,include
from . import views

urlpatterns = [
  path('purchase/<int:product_id>/', views.product_purchase, name='product_purchase'),
  path('successful/', views.payment_successful, name='successful'),
  path('cancelled/', views.payment_cancelled, name='cancelled'),
  path('paypal', include('paypal.standard.ipn.urls'), name='paypal-ipn'),
]