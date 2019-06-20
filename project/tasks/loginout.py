from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.views.generic import FormView
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout
)
from rest_framework.authtoken.models import Token

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print("Username %s added to the database" % username)
            raw_password = form.cleaned_data.get('password1')
            authenticate(username=username, password=raw_password)
            return JsonResponse({"info": "Registered"})
        else:
            return JsonResponse({"info": "Wrong credentials"})
    else:
        return JsonResponse({"info": "Registration"})


class Login(FormView):
    form_class = AuthenticationForm
    authentication_form = None

    def get(self, request, *args, **kwargs):
        return JsonResponse({"info": "Log in page"})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse({"info": "Wrong credentials"})

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        try:
            token = Token.objects.get(user=form.get_user()).key
        except Token.DoesNotExist:
            Token.objects.create(user=form.get_user())
            token = Token.objects.get(user=form.get_user()).key
        return JsonResponse({"info": "Welcome",
                             'token': token})

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class Logout(LogoutView):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return JsonResponse({"info": "Logged out"})
