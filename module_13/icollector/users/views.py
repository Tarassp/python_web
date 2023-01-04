from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from .forms import LoginForm, ProfileForm, RegistrationForm
from .models import User, EmailVerification
from common.views import TitleMixin
from django.shortcuts import redirect


class LoginView(TitleMixin, LoginView):
    title = 'Login - iCollector'
    template_name = 'users/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('index')


class RegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    title = 'Registration - iCollector'
    template_name = 'users/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')
    success_message = "You have successfully registered"


class ProfileView(TitleMixin, SuccessMessageMixin, UpdateView):
    model = User
    title = 'Profile - iCollector'
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_message = " Profile has updated successfully"

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Email Verification - iCollector'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return redirect(to='index')

