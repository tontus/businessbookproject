
from django.urls import path,include
from django.views.generic import TemplateView
from . import views


urlpatterns = [
	path('',views.dashboard,name='dashboard'),
	path('add_fund/',views.add_fund,name='add_fund'),
	path('payment_success/',views.payment_success,name='payment_success'),
	path('payment_failed/',views.payment_failed,name='payment_failed'),
	path('payment_status/',views.payment_status,name='payment_status')

	]
    
