from flask import Response
from rest_framework import viewsets, status
from .models import User, Expense
from .serializers import UserSerializer, ExpenseSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Извлекаем данные из сериализатора
            amount = serializer.validated_data['amount']
            description = serializer.validated_data['description']
            user = serializer.validated_data['user']
            # Создаем новый расход через менеджер
            expense = Expense.objects.create_expense(amount, description, user)
            return Response(ExpenseSerializer(expense).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Реализация метода submitData
    def submitData(self, request):
        # Получаем данные из запроса
        amount = request.data.get('amount')
        description = request.data.get('description')
        user_id = request.data.get('user_id')

        if not amount or not description or not user_id:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)  # Получаем пользователя по ID
        except User.DoesNotExist:
            return Response({'error': 'User  not found'}, status=status.HTTP_404_NOT_FOUND)

        # Создаем новый расход
        expense = Expense.objects.create_expense(amount=amount, description=description, user=user)

        return Response(ExpenseSerializer(expense).data, status=status.HTTP_201_CREATED)