from django.views.generic import TemplateView
from accounts.forms import LoginForm, CustomUsercreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from django.urls import reverse

from django.shortcuts import redirect


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
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return redirect('login')
        print(user.get_username())
        print(user.is_authenticated)
        login(request,user)
        return redirect('task_list')
        
def logout_view(request):
    logout(request)
    return redirect('task_list')


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUsercreationForm
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
