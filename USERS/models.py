from django.db import models
from django.contrib.auth.models import User
from payment.code_generator import refcode
from django.utils import timezone
import os


class profile(models.Model):
    user_name = models.OneToOneField(User,on_delete=models.CASCADE)
    cell_number = models.IntegerField(default=0)
    is_anon_agent = models.BooleanField(default=False)
    is_sales_agent = models.BooleanField(default=False)
    commission = models.IntegerField(default=0)

    def get_valid_cellnumber(self):
        """regex used to validate phone number input"""
        number=self.cell_number
        pass


    def __str__(self):
        return self.user_name.username


class PromoCode(models.Model):
    token = models.CharField(max_length=20)
    owner = models.ForeignKey(profile,on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=False)

    def get_valid_code(user_profile,token):
        access_token = token
        if access_token == None:
            access_token = refcode()
        else:
            if user_profile.is_sales_agent:
                return access_token
            else:
                delta = timezone.now() - access_token.created_at
                minutes = (delta.total_seconds()//60)
                hrs = minutes//60
                days= hrs//24
                print('minutes: ', minutes)
                #print('created at:',access_token.created_at)
                if minutes > 10: #change to 2 weeks in production
                    trash = PromoCode.objects.filter(owner=user_profile)
                    trash.delete()
                    new_token= PromoCode.objects.create(
                        token = user_profile.user_name.username+'-'+refcode(),
                    	owner = user_profile,
                    	created_at = timezone.now(),
                    )

                    access_token=new_token

        return access_token


    def __str__(self):
        return self.token#(f'token : {self.token} belonging to -> {self.owner.user_name.username} ')
