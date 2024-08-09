from decimal import Decimal
from django.db import models
from users.models import User


class Transaction(models.Model):
    amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'), editable=False
    )
    payer = models.ForeignKey(
        User,
        related_name='payer_transactions',
        on_delete=models.CASCADE,
        editable=False,
    )
    payee = models.ForeignKey(
        User,
        related_name='payee_user',
        on_delete=models.CASCADE,
        editable=False,
    )
    date = models.DateTimeField(auto_now_add=True, editable=False)



    def __str__(self):
        return f'from {self.payer.first_name} to {self.payee.first_name} - R$ {self.amount}'