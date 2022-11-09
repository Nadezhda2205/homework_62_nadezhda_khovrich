from django.views.generic import TemplateView
from accounts.forms import LoginForm, CustomUserСreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse



class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('login')

        username: str = form.cleaned_data.get('username')
        password: str = form.cleaned_data.get('password')
        user: User | None = authenticate(request=request, username=username, password=password)

        next: str = request.GET.get('next')

        if not user:
            if next:
                return redirect(reverse('login') + f'?next={next}')
            else:
                return redirect('login')

        login(request, user)

        if next:
            return redirect(next)

        return redirect('task_list')
        
def logout_view(request):
    logout(request)
    return redirect('task_list')


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserСreationForm
    succes_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
        context = {}
        context['form'] = form
        return self.render_to_response(context)


class GroupPermission(UserPassesTestMixin):
    groups = []

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.groups).exists()
