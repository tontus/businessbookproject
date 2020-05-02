from django.shortcuts import render,redirect
from .forms import user_account_form
from django.contrib import messages
from django_email_verification import sendConfirm
from django.core.mail import send_mail
from .models import User
import requests
import json
from django.contrib import auth


def signup(request):
	if request.method=='GET':
		form=user_account_form()
		return render(request,'accounts/signup.html',{'form':form})

	if request.method=='POST':
		form=user_account_form(request.POST)

		if form.is_valid():
			first_name	=	form.cleaned_data['first_name']
			last_name	=	form.cleaned_data['last_name']
			email 		=	form.cleaned_data['email']
			mobile		=	form.cleaned_data['mobile']
			address		=	form.cleaned_data['address']
			country		=	form.cleaned_data['country']
			company		=	form.cleaned_data['company']
			password   	=	form.cleaned_data['password']
			confirm_password = form.cleaned_data['confirm_password']

			response=request.POST['g-recaptcha-response']
			secret_key='6Lewpu0UAAAAABkPKzBhc2Jy_qXJY1HKxJL7pfLP'

			sending_request=requests.post('https://www.google.com/recaptcha/api/siteverify',data={'response':response,'secret':secret_key})
			status=json.loads(sending_request.text)['success']

			if status==False:
				return render(request,'accounts/signup.html',{'form':form,'captcha':'false'})



			if password != confirm_password:
				messages.error(request,'password did not match')
				return render(request,'accounts/signup.html',{'form':form})

			try:
				User.objects.get(email=email)
				return render(request,'accounts/signup.html',{'form':form,'userexist':'true'})
			except User.DoesNotExist:
				create_user=User.objects.create_user(password=password,first_name=first_name,last_name=last_name,email=email,mobile=mobile,address=address,country=country,company=company)
				#send_mail('sub','content','admin@webheavenit.com',[email])
				sendConfirm(create_user)
				return render(request,'accounts/activation.html')


		

		


		return render(request,'accounts/signup.html',{'form':form})




def login(request):
	if request.method=='GET':


		if request.user.is_authenticated == True:
			
			return redirect('dashboard')
		else:
			
			return render(request,'accounts/login.html')

	if request.method=='POST':
		email=request.POST['loginEmail']
		password=request.POST['loginPassword']
		remember=''

		
		authen=auth.authenticate(request,email=email,password=password)
		try:
			r=request.POST['remember']
			if r=='yes':
				remember='yes'
		except:
			remember=''
				

		if authen is not None:

			auth.login(request,authen)

			if remember=='yes':

				request.session['email'] = email

			

			return redirect('dashboard')

		else:
			return render(request,'accounts/login.html',{'error':'email or password is wrong'})



def logout(request):
	
	auth.logout(request)
	return redirect('login')






