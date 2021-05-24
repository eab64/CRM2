from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, CreateUserForm


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status= "Delivered").count()
    pending = orders.filter(status= "Pending").count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_orders':total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {
        'products':products
    }
                  )

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer, 'orders':orders, 'order_count':order_count}
    return render(request, 'accounts/customer.html', context)

def createOrder(request):
    form = OrderForm
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}

    return render(request,'accounts/order_form.html' , context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)


def main(request):
    return render(request,'accounts/main.html' )



def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Регистрация прошла успешна')
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
    context = {}
    return render(request, 'accounts/login.html', context)
