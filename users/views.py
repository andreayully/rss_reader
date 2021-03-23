from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User

from users.forms import SignUpForm


class UserCreateView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup_user.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        form.save()
        return super(UserCreateView, self).form_valid(form)
