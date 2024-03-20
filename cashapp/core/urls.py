from django.urls import path

from .views import AccountTransferApiView, LoginView, UserRegistrationApiView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('register/', UserRegistrationApiView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    #
    # path('logout/', LogoutView.as_view()),
    path('transfer/', AccountTransferApiView.as_view()),
    path('api-auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]