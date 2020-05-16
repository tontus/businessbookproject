from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpRequest

import random
from .models import *
from accounts.models import User

@login_required(login_url='/accounts/login/')
def dashboard(request):
	return render(request,'dashboard/dashboard.html')

@csrf_exempt
def payment_success(request):

	if request.method=="POST":
		payee_account=request.POST['PAYEE_ACCOUNT']
		if payee_account == 'U24170548':
			return render(request,'dashboard/funding_success.html')
		else:
			HttpResponse('sorry,something went wrong')
	else:
		return HttpResponse('wrong destination')



@csrf_exempt
def payment_failed(request):
	if request.method == "POST":


		return render(request,'dashboard/funding_failed.html')

	else:
		return HttpResponse('wrong destination')



@login_required
def add_fund(request):
	if request.session.has_key('order_number'):
		del request.session['order_number']
		del request.session['user_id']

	user_id=request.user.id
	order_number=random.randint(100,999)

	request.session['user_id']=user_id
	request.session['order_number']=order_number





	return render(request,'dashboard/add_fund.html',{'user_id':user_id,'order_number':order_number})




@csrf_exempt
def payment_status(request):
	if request.method=="POST":

		payee_account=request.POST['PAYEE_ACCOUNT']
		amount=float(request.POST['PAYMENT_AMOUNT'])
		payeer_account=request.POST['PAYER_ACCOUNT']
		order_number=request.POST['ORDER_NUM']
		user_id=request.POST['CUST_NUM']

		if payee_account == 'U24170548':
			usr=User.objects.get(id=int(user_id))
			bal=balance.objects.get(user=usr)
			curr_bal=float(bal.current_balance)
			bal.current_balance=(curr_bal+amount)
			bal.save()
			return HttpResponse('success')
		else:
			return HttpResponse('failed payment')

	else:
		return HttpResponse('failed')



