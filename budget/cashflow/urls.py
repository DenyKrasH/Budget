from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from cashflow.views import index, RegisterView, CategoryCreate, AccountCreate, \
    CategoryUpdate, BudgetCreate

urlpatterns = [
    path('<int:budget_pk>', index, name='index'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:budget_pk>/category/create/', CategoryCreate.as_view(),
         name='category-create'),
    path('category/update/<int:pk>/', CategoryUpdate.as_view(),
         name='category-update'),
    path('account/create', AccountCreate.as_view(), name='account-create'),
    path('budget/create', BudgetCreate.as_view(), name='budget-create'),
]
