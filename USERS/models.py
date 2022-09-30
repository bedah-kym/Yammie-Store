from django.db import models
from django.contrib.auth.models import User


class profile(models.Model):
    user_name = models.OneToOneField(User,on_delete=models.CASCADE)
    cell_number = models.IntegerField(default=0)


    def __str__(self):
        return self.user_name.username
# Create your models here.
