from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView

from budget import settings
from cashflow.models import Budget, Category, Account


def index(request):
    return HttpResponse('Main')


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(RegisterView, self).get(*args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

            Account.objects.create(user=user)

            budget = Budget.objects.create()
            budget.user.add(user)

            Category.objects.create(name='Eating out', budget=budget)
            Category.objects.create(name='Food', budget=budget)
            Category.objects.create(name='Entertainment', budget=budget)
            Category.objects.create(name='House', budget=budget)
            Category.objects.create(name='Transport', budget=budget)
            Category.objects.create(name='Clothes', budget=budget)
            Category.objects.create(name='Health', budget=budget)
            Category.objects.create(name='Gift', budget=budget)

            Category.objects.create(name='Salary', type=2, budget=budget)
            Category.objects.create(name='Sale', type=2, budget=budget)
            Category.objects.create(name='Refunds', type=2, budget=budget)
        return super(RegisterView, self).form_valid(form)
