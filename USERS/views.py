from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404
from .forms import registration_form,profileupadateform
from django.contrib import messages
from Shop.models import Cart


def registerview(request):

    if request.method == "POST":
        form = registration_form (request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            form.save()
            messages.success(request,f'WELCOME {username} you can now shop')
            return redirect('users:login')
        messages.warning(request,'invalid credentials')
        return redirect('users:register')
    else:
        form = registration_form()
    return render(request,'USERS/register.html',{'form':form})

@login_required
def profileview(request):
    user= request.user
    user_profile=user.profile
    orders = get_list_or_404(Cart,owner=user)
    #print(orders)
    p_form = profileupadateform()
    if request.method == "POST":
        p_form = profileupadateform(request.POST,instance=user_profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('users:profile')
        else:
            return redirect('users:profile')

    context= {
        'user_profile':user_profile,
        'user' :user,
        'orders':orders,
        'p_form':p_form
    }
    return render(request,'USERS/user-profile.html',context)
