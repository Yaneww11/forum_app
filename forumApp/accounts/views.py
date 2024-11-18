from django.urls import reverse_lazy
from django.views.generic import CreateView
from forumApp.accounts.forms import CustomUserForm


class UserRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserForm
    success_url = reverse_lazy('index')