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

@permission_classes([IsAuthenticated])
class LoginView(APIView):
    # permission_classes = (AllowAny,)
    # serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # serializer = LoginSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data
        # serializer = LoginSerializer(user)
        # token = RefreshToken.for_user(user)
        # data = serializer.data
        # data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response({"message": "success"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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


@permission_classes([IsAuthenticated])
class AccountDeposit(APIView):
    def post(self, request):
        deposit_amount = request.data['amount']
        from_ = request.data['from_']
        desc = request.data['description']
        currency = request.data['currency']
        account = Account.objects.get(account_holder=request.user.id, currency=currency)
        account.account_balance = account.account_balance + deposit_amount
        account.save()
        data = transaction(from_, request.user.id, desc, deposit_amount)
        return Response({'message': "Deposit successful", 'data': data}, status=status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
class MerchantDeposit(APIView):
    def post(self, request):
        pass


@permission_classes([IsAuthenticated])
class Withdraw(APIView):
    def post(self, request):
        amount = request.data['amount']
        to_account = request.data['to']
        desc = request.data['description']
        account = Account.objects.get(account_holder=request.user.id)
        if account.account_balance < amount:
            return Response({'message': 'insufficient balance!'})

        account.account_balance = account.account_balance - amount
        account.save()
        data = transaction(request.user.id, to_account, desc, amount)
        return Response({'message': 'Withdrawal successful!', 'data': data})


def transaction(from_, account, description, amount):
    data = {
        'transaction_id': str(uuid.uuid4()),
        'from_account': from_,
        'to_account': account,
        'amount': amount,
        'description': description,
        'status': 'CO'
    }
    create_transaction = TransactionSerializer(data=data)
    create_transaction.is_valid(raise_exception=True)
    create_transaction.save()
    return create_transaction.data


@permission_classes([IsAuthenticated])
class AccountBalance(APIView):
    def get(self, request):
        account = Account.objects.get(account_holder=request.user.id)
        balance = account.account_balance
        return Response({'balance': balance})
