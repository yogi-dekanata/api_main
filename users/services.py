from decimal import Decimal

from django.utils import timezone

from users.models import User, Transfer, Payment, TopUp

class UserService:
    @staticmethod
    def update_profile(user: User, data: dict) -> User:

        for field, value in data.items():
            if hasattr(user, field) and field != 'phone_number':
                setattr(user, field, value)
        user.save()
        return user

    @staticmethod
    def get_transactions(user: User):

        transfers = Transfer.objects.filter(user=user)
        payments = Payment.objects.filter(user=user)
        top_ups = TopUp.objects.filter(user=user)

        return {
            'transfers': transfers,
            'payments': payments,
            'top_ups': top_ups
        }

    @staticmethod
    def perform_transfer(user: User, target_user_uuid: str, amount: Decimal, remarks: str) -> Transfer:

        if user.balance < amount:
            raise ValueError("Balance is not enough")

        try:
            target_user = User.objects.get(uuid=target_user_uuid)
        except User.DoesNotExist:
            raise ValueError("Target user not found")

        if target_user == user:
            raise ValueError("Cannot transfer to yourself")

        balance_before = user.balance
        balance_after = balance_before - amount

        transfer = Transfer.objects.create(
            user=user,
            target_user=target_user,
            amount=amount,
            remarks=remarks,
            balance_before=balance_before,
            balance_after=balance_after,
            created_date=timezone.now()
        )

        user.balance = balance_after
        target_user.balance += amount
        user.save()
        target_user.save()

        return transfer

    @staticmethod
    def perform_top_up(user: User, amount: Decimal) -> TopUp:

        if amount <= 0:
            raise ValueError("Invalid top-up amount")

        balance_before = user.balance
        balance_after = balance_before + amount

        top_up = TopUp.objects.create(
            user=user,
            amount_top_up=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            created_date=timezone.now()
        )

        user.balance = balance_after
        user.save()

        return top_up

    @staticmethod
    def perform_payment(user: User, amount: Decimal, remarks: str) -> Payment:

        if amount <= 0:
            raise ValueError("Invalid payment amount")

        if user.balance < amount:
            raise ValueError("Balance is not enough")

        balance_before = user.balance
        balance_after = balance_before - amount

        payment = Payment.objects.create(
            user=user,
            amount=amount,
            remarks=remarks,
            balance_before=balance_before,
            balance_after=balance_after,
            created_date=timezone.now()
        )

        user.balance = balance_after
        user.save()

        return payment
