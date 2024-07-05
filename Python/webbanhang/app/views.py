from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {'products': products }
    return render(request,'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer =customer,complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
    context = {'items' :items, 'order': order }
    return render(request,'app/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer =customer,complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
    context = {'items' :items, 'order': order }
    return render(request,'app/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order,created = Order.objects.get_or_create(customer =customer,complete = False)
    orderItem,created = Order.objects.get_or_create(order =order,product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe = False)
    

def register(request):
    form = UserCreationForm()
    
    if request.method == "POST":
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
    context ={'form':form}
    return render(request,'app/register.html',context)
def login(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username= username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'sai con me m roi!')
    context ={}
    return render(request,'app/login.html',context)  