from django.shortcuts import redirect, render
from .models import TrackingHistory,CurrentBalance
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if not user.exists():
            messages.success(request,"User not exist")
            return redirect('login_view')
        user=authenticate(username=username,password=password)
        if not user:
            messages.success(request,"incorrect password")
            return redirect('login_view')
        login(request,user)
        return redirect('index')
    return render(request,'login.html')

def register_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.success(request,"Username is already taken!")
            return redirect('register_view')
        user=User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        messages.success(request,"User name is created")
        return redirect('register_view')
    return render(request,'register.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')





@login_required(login_url='login_view')
def index(request):
    if request.method=='POST':
        amount=request.POST.get('amount')
        description=request.POST.get('description')

        current_balance,_=CurrentBalance.objects.get_or_create(id=1)

        if   amount=="" or float(amount)==0:
            messages.warning(request, "amount not equal to zero")
            return redirect('index')

        expense_type='CREDIT'
        if float(amount)<0:
            expense_type='DEBIT'
        

        
        expense=TrackingHistory.objects.create(
            amount=amount,
            description=description,
            expense_type=expense_type,
            current_balance=current_balance
        )
        current_balance.current_balance+=float(expense.amount)
        current_balance.save()
        return redirect('index')
    current_balance,_=CurrentBalance.objects.get_or_create(id=1)
    income=0
    expense=0
    for tracking_history in TrackingHistory.objects.all():
        if tracking_history.expense_type=='CREDIT':
            income+=float(tracking_history.amount)
        else:
            expense+=float(tracking_history.amount)
    context={
        'transactions':TrackingHistory.objects.all(),
        'current_balance':current_balance,
        'income':income,
        'expense':expense
    }
    return render(request,'index.html',context)

def delete_history(request,id):
    tracking_history=TrackingHistory.objects.filter(id=id)
    if tracking_history.exists():
        current_balance,_=CurrentBalance.objects.get_or_create(id=1)
        tracking_history=tracking_history[0]
        current_balance.current_balance=current_balance.current_balance-tracking_history.amount
        current_balance.save()
    tracking_history.delete()
    return redirect('index')