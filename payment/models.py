from django.db import models
from Shop.models import Cart
from django.contrib.auth.models import User

# Create your models here.
class payment_info(models.Model):
    phone_number = models.IntegerField()
    amount = models.IntegerField(default=0)
    cart_number = models.ForeignKey(Cart,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
