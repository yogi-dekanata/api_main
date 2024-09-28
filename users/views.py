from decimal import Decimal

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (ProfileUpdateSerializer, TopUpSerializer, TransferSerializer, PaymentSerializer)
from .services import UserService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if User.objects.filter(phone_number=data['phone_number']).exists():
            return Response({'message': 'Phone Number already registered'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            phone_number=data['phone_number'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            pin=data['pin']
        )
        return Response({
            'status': 'SUCCESS',
            'result': {
                'user_id': user.uuid,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'address': user.address,
                'created_date': user.date_joined
            }
        }, status=status.HTTP_201_CREATED)


# Login API
# Login API
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        pin = request.data.get('pin')

        # Gunakan custom backend untuk phone_number
        user = authenticate(request, phone_number=phone_number, password=pin)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'SUCCESS',
                'result': {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                }
            })
        else:
            return Response({'message': 'Phone Number and PIN doesn’t match.'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            updated_user = UserService.update_profile(user, serializer.validated_data)
            return Response({
                "status": "SUCCESS",
                "result": ProfileUpdateSerializer(updated_user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionsReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        transactions = UserService.get_transactions(user)
        transfer_serializer = TransferSerializer(transactions['transfers'], many=True)
        payment_serializer = PaymentSerializer(transactions['payments'], many=True)
        top_up_serializer = TopUpSerializer(transactions['top_ups'], many=True)

        all_transactions = transfer_serializer.data + payment_serializer.data + top_up_serializer.data

        all_transactions.sort(key=lambda x: x['created_date'], reverse=True)

        return Response({
            'status': 'SUCCESS',
            'result': all_transactions
        }, status=status.HTTP_200_OK)


class TopUpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        amount = request.data.get('amount')

        try:
            top_up = UserService.perform_top_up(user, Decimal(amount))
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TopUpSerializer(top_up)
        return Response({
            "status": "SUCCESS",
            "result": serializer.data
        }, status=status.HTTP_201_CREATED)


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        target_user_uuid = request.data.get('target_user')
        amount = request.data.get('amount')
        remarks = request.data.get('remarks')

        try:
            transfer = UserService.perform_transfer(user, target_user_uuid, Decimal(amount), remarks)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransferSerializer(transfer)
        return Response({
            "status": "SUCCESS",
            "result": serializer.data
        }, status=status.HTTP_201_CREATED)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        remarks = request.data.get('remarks')

        try:
            payment = UserService.perform_payment(user, Decimal(amount), remarks)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaymentSerializer(payment)
        return Response({
            "status": "SUCCESS",
            "result": serializer.data
        }, status=status.HTTP_201_CREATED)
