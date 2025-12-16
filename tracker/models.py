from django.db import models


# Create your models here.
class CurrentBalance(models.Model):
    current_balance=models.FloatField(default=0)
    create_at=models.DateTimeField(auto_now=True)
    update_at=models.DateTimeField(auto_now_add=True)

class TrackingHistory(models.Model):
    amount=models.FloatField()
    description=models.CharField(max_length=300)
    expense_type = models.CharField(choices=(('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')), max_length=200)
    current_balance=models.ForeignKey(CurrentBalance,on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now=True)
    update_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"The amount is {self.amount} for {self.description} expense type is {self.expense_type}"