from django.shortcuts import redirect, render
from .models import TrackingHistory,CurrentBalance
from django.contrib import messages

# Create your views here.
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