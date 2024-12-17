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

        # Метод для получения одной записи по ID
        def retrieve(self, request, pk=None):
            try:
                expense = self.get_object()  # Получаем объект по ID
                return Response(ExpenseSerializer(expense).data, status=status.HTTP_200_OK)
            except Expense.DoesNotExist:
                return Response({'error': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)

        # Метод для редактирования записи
        def partial_update(self, request, pk=None):
            try:
                expense = self.get_object()  # Получаем объект по ID
                if expense.status != Expense.NEW:
                    return Response({'state': 0, 'message': 'Only expenses with status "new" can be edited.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Обновляем поля, кроме тех, что содержат ФИО, адрес почты и номер телефона
                for field in ['amount', 'description']:
                    if field in request.data:
                        setattr(expense, field, request.data[field])
                expense.save()  # Сохраняем изменения

                return Response({'state': 1, 'message': 'Expense updated successfully.'}, status=status.HTTP_200_OK)
            except Expense.DoesNotExist:
                return Response({'state': 0, 'message': 'Expense not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Метод для получения всех расходов пользователя по email
        def list(self, request):
            email = request.query_params.get('user__email')
            if email:
                try:
                    user = User.objects.get(email=email)
                    expenses = Expense.objects.filter(user=user)
                    return Response(ExpenseSerializer(expenses, many=True).data, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'error': 'User  not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Email parameter is required'}, status=status.HTTP_400_BAD_REQUEST)