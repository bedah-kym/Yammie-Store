from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404
from .forms import registration_form,profileupadateform,profileimageupdateform
from django.contrib import messages
from Shop.models import Cart
from django.utils import timezone
from django.http import Http404
from .models import profile,PromoCode
from payment.code_generator import refcode
from django.contrib.auth.models import User

#reportlab imports
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



def registerview(request):

    if request.method == "POST":
        form = registration_form (request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            form.save()
            messages.warning(request,f'WELCOME {username} please add your phone number to continue')
            return redirect('users:profile')
        #print(form.errors)
        messages.warning(request,form.errors)
        return redirect('users:register')
    else:
        form = registration_form(request.POST)
    return render(request,'USERS/register.html',{'form':form})

@login_required
def makeagent(request):
    user = request.user
    user_profile=user.profile
    try:
        qs = get_object_or_404(profile,user_name=user,is_anon_agent=False)
    except Http404:
        return redirect('users:profile')
    if user_profile.cell_number >0: #use a valid check
        code=PromoCode.objects.create(
            token = user_profile.user_name.username+'-'+refcode(),
        	owner = request.user.profile,
        	created_at = timezone.now(),
        )
        qs.is_anon_agent=True
        qs.save()
    else:
        messages.warning(request,"Please put in your active phone number")
        return redirect('users:profile')

    return redirect('users:profile')

@login_required
def unmakeagent(request):
    user = request.user
    user_profile=user.profile
    try:
        qs = get_object_or_404(profile,user_name=user,is_anon_agent=True,is_sales_agent=False)

    except Http404:
        return redirect('users:profile')

    qs.is_anon_agent=False
    qs.commission=0
    qs.save()
    messages.info(request,"you are now a regular user")

    return redirect('users:profile')

@login_required
def profileview(request):
    user= request.user
    user_profile=user.profile
    valid_code=''
    created=''
    orders=[]
    try:
        orders = Cart.objects.filter(owner=user,ordered=True).order_by('-order_date')
    except Http404:
        orders=[]
    #this is for agents to get their valid agent code
    if user_profile.is_anon_agent or user_profile.is_sales_agent:
        code = get_list_or_404(PromoCode,owner=user_profile)[0]
        valid_code = PromoCode.get_valid_code(user_profile,code)
        created = valid_code.created_at
        #phone numberupdate form
    p_form = profileupadateform(request.POST)
    dp_form = profileimageupdateform()
    if request.method == "POST":
        p_form = profileupadateform(request.POST,instance=user_profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('users:profile')
        else:
            messages.info(request,"Sorry! number should have nine digits")
            return redirect('users:profile')


    context= {
        'user_profile':user_profile,
        'user' :user,
        'orders':orders,
        'dp_form':dp_form,
        'p_form':p_form,
        'code':valid_code,
        'created':created
    }
    return render(request,'USERS/user-profile.html',context)

@login_required
def pdf_order_download(request):
    #find the users orders
    try:
        orders = Cart.objects.filter(owner=request.user,ordered=True).order_by('-order_date')
    except Http404:
        orders=[]
        return redirect('users:profile')

    if len(orders) >0 :
        #bytestream buffer
        buffer = io.BytesIO()
        #canvas to hold the data
        c= canvas.Canvas(buffer ,pagesize=letter, bottomup=0)
        #textobject
        textob = c.beginText()
        textob.setTextOrigin(inch,inch)
        textob.setFont('Helvetica',15)
        #list to store the lines
        orderlist=[]
        counter=0
        #write all the orders line by line
        for order in orders:
            counter+=1
            orderlist.append(str(counter))
            orderlist.append('Date ordered :'+     str(order.order_date))
            orderlist.append('Ordered by :' +      str(order.owner.username))
            orderlist.append('Cart number :'+      str(order.ref_code))
            orderlist.append('total price :'+      str(order.total_price))
            orderlist.append('payment method :'+    str(order.payment_method))
            orderlist.append('Agent confirmed ?:'+ str(order.agent_confirmed))
            orderlist.append('Agent promocode :'+ str(order.agent_code))
            orderlist.append("----------------------------  ")

        for orderitem in orderlist:
            textob.textLine(orderitem)

        #close up
        c.drawText(textob)
        c.showPage()
        c.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='Mysoko_all_orders.pdf')
    else:
        messages.warning(request,'you have no complete orders!')
        return redirect('users:profile')

@login_required
def single_pdf_order_download(request):

    #find the users orders
    try:
        orders = Cart.objects.filter(owner=request.user,ordered=True)[::-1]
        order = orders[0]
        
    except Http404:
        messages.warning("you have no orders!")
        return redirect('users:profile')


    #bytestream buffer
    buffer = io.BytesIO()
    #canvas to hold the data
    c= canvas.Canvas(buffer ,pagesize=letter, bottomup=0)
    #textobject
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont('Helvetica',15)
    #list to store the lines
    orderlist=[]
    counter=0
    #write all the orders line by line
    orderlist.append('Date ordered :'+     str(order.order_date))
    orderlist.append('Ordered by :' +      str(order.owner.username))
    orderlist.append('Cart number :'+      str(order.ref_code))
    orderlist.append('total price :'+      str(order.total_price))
    orderlist.append('payment method :'+    str(order.payment_method))
    orderlist.append('Agent confirmed ?:'+ str(order.agent_confirmed))
    orderlist.append('Agent promocode :'+ str(order.agent_code))
    orderlist.append("----------------------------.............. ")



    for orderitem in orderlist:
        textob.textLine(orderitem)

    #close up
    c.drawText(textob)
    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Mysoko_single_order.pdf')





def profilepicupdate(request):
    user= request.user
    user_profile=request.user.profile
    dp_form = profileimageupdateform()
    if request.method == "POST" :
        print(request.FILES)
        dp_form = profileimageupdateform(request.POST,request.FILES,instance=user_profile)
        if dp_form.is_valid():
            dp_form.save()
            return HttpResponseRedirect('/users/profile/')
        else:
            messages.info(request,dp_form.errors)
            return redirect('users:profile')
