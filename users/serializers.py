from rest_framework import serializers
from .models import TopUp, Payment, Transfer

class TopUpSerializer(serializers.ModelSerializer):
    transaction_type = serializers.CharField(default='CREDIT')

    class Meta:
        model = TopUp
        fields = ['id', 'amount_top_up','transaction_type', 'balance_before', 'balance_after', 'created_date']



class PaymentSerializer(serializers.ModelSerializer):
    transaction_type = serializers.CharField(default='DEBIT')

    class Meta:
        model = Payment
        fields = ['id', 'uuid', 'amount', 'transaction_type','remarks', 'balance_before', 'balance_after', 'created_date']
        read_only_fields = ['id', 'uuid', 'balance_before', 'balance_after', 'created_date']



class TransferSerializer(serializers.ModelSerializer):
    transfer_id = serializers.UUIDField(source='uuid')
    transaction_type = serializers.CharField(default='DEBIT')

    class Meta:
        model = Transfer
        fields = ['transfer_id', 'amount','transaction_type', 'remarks', 'balance_before', 'balance_after', 'created_date']


from users.models import User

class ProfileUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='id', read_only=True)
    updated_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'address', 'updated_date']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'address': {'required': True},
        }
