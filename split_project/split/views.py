from django.contrib.auth.models import User
from flask import Response
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView

from .models import  Expense
from .serializers import  ExpenseSerializer


class ExpenseCreateAPIView(CreateAPIView):
    """Создание перевала"""

    queryset = Expense.objects.filter(id=0)
    serializer_class = ExpenseSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            response_data = {}

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'message': '',
                    'id': serializer.data.get('id')
                }
            else:
                response_data = {
                    'status': 400,
                    'message': 'Неверный запрос',
                    'id': serializer.data.get('id')
                }
        except:
            response_data = {
                'status': 500,
                'message': 'Ошибка подключения к базе данных',
                'id': serializer.data.get('id')
            }


        return Response(response_data)


class ExpenseUpdateAPIView(UpdateAPIView):
    """Обновление данных перевала"""

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def partial_update(self, request, *args, **kwargs):

        pereval = self.get_object()
        serializer = self.serializer_class(pereval, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 200,
                'message': 'Данные успешно изменены',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'status': 400,
                'message': 'Данные о пользователе нельзя изменять',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



class ExpenseListAPIView(ListAPIView):
    """Вывод списка перевалов, добавленных пользователем"""

    def get(self, request, email):
        perevals = Expense.objects.filter(user__email=email).order_by('id')
        serializer = ExpenseSerializer(perevals, many=True)

        return Response(serializer.data)