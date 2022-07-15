from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Account')
    balance = models.FloatField(default=0)

    def __str__(self):
        return f'User: {self.user.username} - {self.name}'


class Budget(models.Model):
    TYPE = [
        (1, 'Personal'),
        (2, 'Overall')
    ]
    user = models.ManyToManyField(User)
    type = models.PositiveSmallIntegerField(choices=TYPE, default=1)
    name = models.CharField(max_length=100, default='Personal budget')


class Category(models.Model):
    TYPE = [
        (1, 'Expenses'),
        (2, 'Income')
    ]
    name = models.CharField(max_length=100)
    type = models.PositiveSmallIntegerField(choices=TYPE, default=1)
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE)

    def __str__(self):
        return f'Budget id: {self.budget.pk} - {self.name}'


class Cashflow(models.Model):
    sum = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    note = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
