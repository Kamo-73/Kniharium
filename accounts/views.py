from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accounts.forms import SignUpForm, ProfileModelForm, UserForm
from accounts.models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'form.html'


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Registrace'
        context['submit_button_text'] = 'Zaregistrovat se'
        return context


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))  # zůstat na stejné stránce


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return get_object_or_404(Profile, user__id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['is_partner'] = profile.user.groups.filter(name='Partners').exists()
        return context

class ProfileUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user__id=kwargs.get("pk"))
        if profile.user != request.user:
            return redirect('home')  # alebo vyhodenie 403 podľa potreby
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        profile = get_object_or_404(Profile, user__id=pk)
        user_form = UserForm(instance=profile.user)
        profile_form = ProfileModelForm(instance=profile)
        return render(request, 'form.html', {
            'form_title': 'Úprava profilu',
            'submit_button_text': 'Uložit změny',
            'user_form': user_form,
            'form': profile_form,
        })

    def post(self, request, pk):
        profile = get_object_or_404(Profile, user__id=pk)
        user_form = UserForm(request.POST, instance=profile.user)
        profile_form = ProfileModelForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', pk=pk)

        return render(request, 'form.html', {
            'form_title': 'Úprava profilu',
            'submit_button_text': 'Uložit změny',
            'user_form': user_form,
            'form': profile_form,
        })
class ProfileDeleteView(DeleteView):
    model = Profile
    template_name = 'confirm_delete.html'
    context_object_name = 'profile'

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return get_object_or_404(Profile, user__id=user_id)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return redirect('home')  # alebo vyhodenie 403
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('home')