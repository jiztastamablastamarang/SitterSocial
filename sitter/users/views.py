from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from rest_framework.decorators import action
from .serializers import UserLoginSerializer, UserRegisterSerializer
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView
import time

class UserLoginView(LoginView):
    serializer_class = UserLoginSerializer


class UserRegisterView(RegisterView):
    serializer_class = UserRegisterSerializer
