from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from .models import Expense
from .serializers import ExpenseSerializer


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
                    'status': 201,
                    'message': '',
                    'id': serializer.data.get('id')
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            response_data = {
                'status': 400,
                'message': serializer.errors,
                'id': serializer.data.get('id')
            }

            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            response_data = {
                'status': 500,
                'message': 'Ошибка подключения к базе данных',
            }

        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpenseRetrieveUpdateAPIView(UpdateModelMixin, RetrieveAPIView):
    """Обновление данных перевала"""

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        serializer = self.serializer_class(pereval, data=request.data, partial=True)

        try:
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'state': 1,
                    'message': 'Данные успешно изменены',
                }
                return Response(response_data, status=status.HTTP_200_OK)

            response_data = {
                'status': 400,
                'state': 0,
                'message': serializer.errors,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            response_data = {
                'status': 500,
                'state': 0,
                'message': 'Ошибка подключения к базе данных',
            }

        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpenseListAPIView(ListAPIView):
    """Вывод списка перевалов, добавленных пользователем"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'user.email'

    def get(self, request, email, *args, **kwargs):
        perevals = Expense.objects.filter(user__email=email)
        serializer = ExpenseSerializer(perevals, many=True)

        return Response(serializer.data)
