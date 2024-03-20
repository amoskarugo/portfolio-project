from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import uuid
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import TransactionSerializer, AccountSerializer, LoginSerializer, UserRegistrationSerializer
from django.contrib.auth import get_user_model, authenticate
from .models import Transaction, Account
from rest_framework.views import Response

User = get_user_model()


# Create your views here.
class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = LoginSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class UserRegistrationApiView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
class AccountTransferApiView(APIView):
    def post(self, request):
        amount = request.data['amount']
        try:

            recipient = User.objects.get(email=request.data['recipient'])
            recipient_account = Account.objects.get(account_holder=recipient.id)
        except User.DoesNotExist:
            return Response({"message": "user not found!"})
        sender = request.user
        account = Account.objects.get(account_holder=sender.id)
        balance = account.account_balance

        if amount > balance:
            return Response({'message': 'insufficient balance!'})

        account.account_balance = balance - amount

        recipient_account.account_balance = recipient_account.account_balance + amount

        recipient_account.save()
        account.save()

        submit_data = {
            'transaction_id': str(uuid.uuid4()),
            'from_account': sender.id,
            'to_account': recipient.id,
            'amount': amount,
            'description': 'T',
            'status': 'CO'
        }
        submit_transaction = TransactionSerializer(data=submit_data)
        submit_transaction.is_valid(raise_exception=True)
        submit_transaction.save()
        return Response(submit_transaction.data)
