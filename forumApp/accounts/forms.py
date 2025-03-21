from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')