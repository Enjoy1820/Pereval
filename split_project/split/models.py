from django.db import models
from dotenv import load_dotenv

load_dotenv()

class User(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExpenseManager(models.Manager):
    def create_expense(self, amount, description, user):

        expense = self.create(amount=amount, description=description, user=user, status='new')
        return expense


class Expense(models.Model):
    NEW = 'new'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (NEW, 'Новый'),
        (PENDING, 'На модерации'),
        (ACCEPTED, 'Принят'),
        (REJECTED, 'Отклонен'),
    ]


    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='expenses', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NEW)

    objects = ExpenseManager()

    def __str__(self):
        return f"{self.description} - {self.amount}"
