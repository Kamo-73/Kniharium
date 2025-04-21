from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from accounts.forms import SignUpForm
from accounts.models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'form.html'


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Registrácia'
        context['submit_button_text'] = 'Zaregistrovať sa'
        return context


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))  # zůstat na stejné stránce


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self):
        user_id = self.kwargs.get("pk")  # toto je z URL (user.id)
        return get_object_or_404(Profile, user__id=user_id)
