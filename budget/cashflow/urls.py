from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from cashflow.views import index, RegisterView

urlpatterns = [
    path('', index),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
