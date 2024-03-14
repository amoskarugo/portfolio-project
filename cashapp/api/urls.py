from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from app.views import TransactionApiView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('transact/', TransactionApiView.as_view()),
    path('api-auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]