from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = User
    balance = models.FloatField(default=0)


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


class Cashflow(models.Model):
    sum = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    note = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
