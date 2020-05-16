from django.db import models
from accounts.models import User


class balance(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	current_balance=models.FloatField(max_length=9,default=0.0)

	def __str__(self):
		return str(self.user.email)

