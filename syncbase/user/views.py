from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import models as model_forms
from django.urls import reverse_lazy as reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from user.forms import NewAccountForm
from user.widgets import RangeInput


class UserCreate(CreateView):
    template_name = "user/create_form.html"
    form_class = NewAccountForm
    success_url = reverse(settings.LOGIN_URL)

    def form_valid(self, form):
        """ Set a valid password on valid form """
        form.instance.set_password(form.cleaned_data.get("password"))
        return super(UserCreate, self).form_valid(form)


class BasicInfo(LoginRequiredMixin, UpdateView):
    template_name = "user/info_basic.html"
    success_url = reverse('user:basic')
    model = User
    fields = ['username', 'email']

    def get_object(self, queryset=None):
        return self.request.user
