from django.urls import path

from .views import AccountTransferApiView, LoginView, UserRegistrationApiView, AccountDeposit, AccountBalance, Withdraw, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('register/', UserRegistrationApiView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    #
    path('logout/', LogoutView.as_view(), name='logout'),
    path('deposit/', AccountDeposit.as_view(), name='deposit'),
    path('withdraw/', Withdraw.as_view(), name='withdraw'),
    path('balance/', AccountBalance.as_view(), name='balance'),
    path('transfer/', AccountTransferApiView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
