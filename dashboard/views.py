from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpRequest
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
from . import models
import random
from .models import *
from accounts.models import User

@login_required(login_url='/accounts/login/')
def dashboard(request):
	bal=balance.objects.get(user=request.user).current_balance

	return render(request,'dashboard/dashboard.html',{'balance':round(bal,2)})

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


@login_required(login_url='/accounts/login/')
def balance_transfer(request):
	if request.method == 'POST':
		toemail=request.POST['toemail']
		amount=float(request.POST['amount'])

		userbalancedata =  balance.objects.get(user=request.user)
		userbalance=userbalancedata.current_balance

		if amount>userbalance :
			messages.warning(request,'dont have enough funds')

			return redirect('send_money')

		try:
			to=balance.objects.get(user__email=toemail)
			userbalancedata.current_balance=round(float(userbalancedata.current_balance - amount),2)
			userbalancedata.save()
			to.current_balance=round(float(to.current_balance + amount),2)
			to.save()

			messages.success(request,'balance transfer successful')
			return redirect('send_money')



		except balance.DoesNotExist :
			messages.info(request,'user does not exist')
			return redirect('send_money')
		


@login_required(login_url='/accounts/login/')
def adpack_list(request):
	adp_list=adpack.objects.all()
	return render(request,'dashboard/adpack-list.html',{'adp_list':adp_list})

@login_required(login_url='/accounts/login/')
def refer_page(request):
	usrid=request.user.id
	refered_user=refer.objects.filter(referer=int(usrid))
	return render(request,'dashboard/refer.html',{'referdata':refered_user})


def buy_adpack(request,level):
	if request.method == 'GET':
		adpdetails=adpack.objects.get(level=level)

		return render(request,'dashboard/buy-adpack.html',{'adpack_details':adpdetails})

	if request.method == 'POST':
		level=request.POST['level']
		quantity=int(request.POST['quantity'])
		user=request.user

		adp=adpack.objects.get(level=int(level))
		total_price=round(float(adp.value*quantity),2)
		total_revenue=round(float(adp.perday_revenue*60*quantity),2)
		perday_revenue=round(float(adp.perday_revenue*quantity),2)
		affiliate_commission=round(float(adp.affiliate_earn*quantity),2)
		affiliate_id=refer.objects.get(user=request.user).referer
		expiration_date=datetime.now()+timedelta(days=60)
		bal=balance.objects.get(user=request.user).current_balance
		max_buy=int(adp.max_buy)
		recent_bought=[]
		for i in range(0,int(level)):
			recent_bought.append(i)

		check=bought_adpack.objects.filter(Q(user=request.user) & Q(expiration_date__gt=datetime.now()) & Q(bought_adpacks__level=int(recent_bought[-1])))

		check_max=bought_adpack.objects.filter(Q(user=request.user) & Q(expiration_date__gt=datetime.now()) & Q(bought_adpacks__level=int(level)))

		if bal<total_price:							
			messages.info(request,'insufficient fund')
			return redirect('buy_adpack',int(level))

		elif len(check)<max_buy and int(level)!=1 :
			messages.warning(request,'you can not buy before buying(max) previous level adpack')
			return redirect('buy_adpack',int(level))

		elif (max_buy-len(check_max))<quantity:
			messages.error(request,'you are allowed to buy only '+(max_buy-len(check_max))+' more adpacks with this package')
			return redirect('buy_adpack',int(level))


		else:
			usrbalance=balance.objects.get(user=request.user)
			usrbalance.current_balance=(usrbalance.current_balance)-total_price
			usrbalance.save()

			adpack_database=bought_adpack()
			adpack_database.user=request.user
			adpack_database.expiration_date=expiration_date
			adpack_database.total_quantity=quantity
			adpack_database.bought_adpacks=adp
			adpack_database.adpack_totalreturn=total_revenue
			adpack_database.everyday_revenue=perday_revenue
			adpack_database.affiliate_commission=affiliate_commission
			adpack_database.total_price=total_price

			adpack_database.save()

			rupdate=refer.objects.get(user=request.user)
			rupdate.refer_earn=round(float(rupdate.refer_earn+affiliate_commission),2)
			rupdate.save()

			messages.success(request,'successfully bought adpack')
			return redirect('buy_adpack',int(level))













