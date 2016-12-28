from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from .forms import LoginForm


class Login(View):
    form_class = LoginForm
    template_name = 'client_login_page/login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('admin_panel:panel')

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('admin_panel:panel')
            else:
                message = 'Invalid login or password'
                message_class = 'alert-danger'
                return render(request, self.template_name, {
                    'form': form,
                    'message': message,
                    'message_class': message_class
                })

        else:
            message = 'Invalid login or password'
            message_class = 'alert-danger'
            return render(request, self.template_name, {
                'form': form,
                'message': message,
                'message_class': message_class
            })


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
        return redirect('client_login_page:client_login')
