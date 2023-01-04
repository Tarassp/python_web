from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', login_required(views.ProfileView.as_view()), name='profile'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/', views.EmailVerificationView.as_view(), name='email_verification'),
]
