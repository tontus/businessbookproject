
from django.urls import path,include
from django.views.generic import TemplateView
from . import views


urlpatterns = [
	path('',views.dashboard,name='dashboard'),
	path('add_fund/',views.add_fund,name='add_fund'),
	path('payment_success/',views.payment_success,name='payment_success'),
	path('payment_failed/',views.payment_failed,name='payment_failed'),
	path('payment_status/',views.payment_status,name='payment_status'),
	path('send_money/',TemplateView.as_view(template_name='dashboard/send-fund.html'),name='send_money'),
	path('balance_transfer/',views.balance_transfer,name='balance_transfer'),
	path('adpack_list/',views.adpack_list,name='adpack_list'),
	path('refer/',views.refer_page,name='refer'),
	path('buy_adpack/<int:level>/',views.buy_adpack,name='buy_adpack'),

	]
    
