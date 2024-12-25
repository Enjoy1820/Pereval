from django.urls import path
from .views import (
    ExpenseRetrieveUpdateAPIView,
    ExpenseCreateAPIView, ExpenseListAPIView
)

urlpatterns = [
    path('submitData/', ExpenseCreateAPIView.as_view()),
    path('submitData/<int:id>', ExpenseRetrieveUpdateAPIView.as_view()),
    path('submitData/user__email=<str:email>/', ExpenseListAPIView.as_view()),
]