from django.views import generic
from .models import User
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    model = User
    success_url = reverse_lazy('tweets:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
