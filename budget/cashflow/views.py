from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, UpdateView

from budget import settings
from cashflow.models import Budget, Category, Account, Cashflow

menu = {'Category': {'title': 'Category', 'url_name': 'account-create'},
        'Budget': {'title': 'Overall budget', 'url_name': 'budget-create'},
        '124': {'title': 'User', 'url_name': 'logout'}}


def index(request, budget_pk):
    cashflows = Cashflow.objects.select_related('category__budget') \
        .filter(category__budget=budget_pk)

    category_expense = Cashflow.objects.select_related('category__budget') \
        .filter(category__budget=budget_pk, category__type=1) \
        .values('category', 'category__name') \
        .annotate(sum=Sum('sum'))

    chart_data = [['Category', 'Sum']]
    for item in category_expense:
        chart_data.append([item['category__name'], item['sum']])

    submenu = [{'title': 'Create budget', 'url_name': 'budget-create'}, ]
    overall_budgets = Budget.objects.filter(user=request.user, type=2)

    for item in overall_budgets:
        submenu.append({'title': item.name, 'url_name': 'index', 'pk': item.pk})

    menu['Budget']['submenu'] = submenu

    context = {'cashflows': cashflows, 'category_expense': category_expense,
               'chart_data': chart_data, 'chart_title': 'Expense chart',
               'menu': menu}

    return render(request, 'cashflow/index.html', context)


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

            Account.objects.create(user=user, name='Cash')
            Account.objects.create(user=user, name='Payment card')

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
        return super().form_valid(form)


class CategoryCreate(CreateView):
    model = Category
    fields = ['name', 'type']
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        budget = Budget.objects.get(pk=self.kwargs['budget_pk'])
        form.instance.budget = budget
        return super().form_valid(form)


class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name', 'type']
    success_url = settings.LOGIN_REDIRECT_URL


class AccountCreate(CreateView):
    model = Account
    fields = ['name', 'balance']
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BudgetCreate(CreateView):
    model = Budget
    fields = ['name', 'type']
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        if form.is_valid():
            budget = form.save()
            budget.user.add(self.request.user)
        return super().form_valid(form)
