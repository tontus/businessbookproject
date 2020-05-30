from django.db import models
from accounts.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class balance(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	current_balance=models.FloatField(max_length=9,default=0.0)

	def __str__(self):
		return str(self.user.email)


class refer(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
	referer=models.IntegerField(null=True,blank=True)
	refer_earn=models.FloatField(blank=True,null=True,default=0)

	def __str__(self):
		return str(self.user.email)


class adpack(models.Model):
	title =  models.CharField(max_length=40)
	value = models.IntegerField()
	level = models.IntegerField(null=True)
	image = models.ImageField(upload_to='adpack-image/')
	perday_revenue = models.FloatField(null=True)
	expiration_day = models.IntegerField(default=60,null=True)
	affiliate_earn = models.FloatField(null=True)
	total_return = models.FloatField(null=True)
	max_buy = models.IntegerField(null=True)

	def __str__(self):
		return str(self.title)



class bought_adpack(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	buying_date=models.DateField(default=datetime.now())
	expiration_date=models.DateField()
	total_quantity=models.IntegerField()
	bought_adpacks=models.ForeignKey(adpack,on_delete=models.CASCADE)
	adpack_totalreturn=models.FloatField()
	everyday_revenue=models.FloatField()
	affiliate_commission=models.FloatField()
	total_price=models.FloatField()


	def __str__(self):
		return str(self.bought_adpack)



