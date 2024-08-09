from ninja import Router
from .schemas import TransactionSchema
from django.shortcuts import get_object_or_404
from users.models import User
from rolepermissions.checkers import has_permission
from django.db import transaction as django_transaction


payments_router = Router()


@payments_router.post('/', response={200: dict, 400: dict, 403: dict})
def transaction(request, transaction: TransactionSchema):
    payer = get_object_or_404(User, id=transaction.payer)
    payee = get_object_or_404(User, id=transaction.payer)

    if payer.amount < transaction.amount:
        return 400, {'error': 'Insufficient funds'}

    if not has_permission(payer, 'make_transfer'):
        return 403, {'error': 'User does not have permission to perform transfers'}

    if not has_permission(payee, 'receive_transfer'):
        return 403, {'error': 'User cannot receive transfers'}

    with django_transaction.atomic():
        payer.pay(transaction.amount)
        payee.receive(transaction.amount)

        transact = transaction(
            amount=transaction.amount,
            payer_id=transaction.payer,
            payee_id=transaction.payee,
        )

        payer.save()
        payee.save()
        transact.save()

    return 200, {'transaction_id': 1}
