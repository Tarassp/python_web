from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.views import LoginView
from .forms import LoginForm, ProfileForm, RegistrationForm
from .models import User
from common.views import TitleMixin


class LoginView(TitleMixin, LoginView):
    title = 'Login - iCollector'
    template_name = 'users/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('index')


class RegistrationView(TitleMixin, CreateView):
    title = 'Registration - iCollector'
    template_name = 'users/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')


class ProfileView(TitleMixin, UpdateView):
    model = User
    title = 'Profile - iCollector'
    template_name = 'users/profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))
