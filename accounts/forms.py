from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from infra.models import CustomUser



class SignupForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ('username',)