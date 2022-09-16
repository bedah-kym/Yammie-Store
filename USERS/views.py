from django.shortcuts import render,redirect
#from django.contrib.auth.models import User
from .forms import registration_form
from django.contrib import messages



def registerview(request):

    if request.method == "POST":
        form = registration_form (request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            form.save()
            messages.success(request,f'WELCOME {username} you can now shop')
            return redirect('users:login')
        return redirect('users:register')
    else:
        form = registration_form()
    return render(request,'USERS/register.html',{'form':form})
