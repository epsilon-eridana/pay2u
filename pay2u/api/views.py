import datetime

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.utils import timezone

from .serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ServiceSerializer
)
from services.models import Category, Service
from users.models import User
from subscriptions.models import Subscription, Payment


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().prefetch_related(
        'services'
    )
    serializer_class = CategoryListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return self.serializer_class


class ServiceViewSet(
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Service.objects.all().prefetch_related(
        'tags',
        'rates',
        'options',
        'images'
    )
    serializer_class = ServiceSerializer

    @action(
        methods=['post', 'put', 'delete'],
        detail=True
    )
    def subscription(self, request, **kwargs):
        """Оформление подписки на сервис."""
        # Проверка: существует ли сервис с таким id.
        # POST, PUT and DELETE
        service = get_object_or_404(
            Service,
            id=kwargs.get('pk')
        )
        user = request.user
        rate_id = request.data.get('rate')
        # Затычка пока нет авторизации
        user = User.objects.get(username='root')
        current_datetime = timezone.now()

        if not (rate := service.rates.filter(
                id=rate_id
        ).first()) and (request.method != 'DELETE'):
            # Проверка: наличия тарифа в теле запроса
            # и есть ли такой тариф у сервиса. POST and PUT
            return Response(
                data='Отсутствует информация о выбранном тарифе.',
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription = user.subscriptions.filter(
            rate__service=service,
            date_end__gt=current_datetime
        )
        if not subscription:
            # Проверка: у пользователя нет активных подписок.
            if request.method == 'DELETE' or request.method == 'PUT':
                return Response(
                    data='У вас нет активных подписок.',
                    status=status.HTTP_400_BAD_REQUEST
                )
            # POST: Создать запись со статусом "ожидает оплаты".
            # Вернуть пользователю ссылку или id записи.
            return Response(
                data={'pay_url': '/'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'POST':
            # POST: Ошибка "Существует активная подписка на сервис."
            return Response(
                data='Существует активная подписка на сервис.',
                status=status.HTTP_400_BAD_REQUEST
            )
        if subscription.rate.id == rate_id and (request.method == 'PUT'):
            # PUT: Проверяем чтобы id тарифа активной подписке
            # не совпадал с тарифом на который хотим сменить.
            return Response(
                data='Существует активная подписка с таким тарифом.',
                status=status.HTTP_400_BAD_REQUEST
            )
        if subscription.extension:
            # PUT and DELETE: Продление включено.
            # Отключить авто-продление, задача
            # проверяет пред продление статус авто-продления.
            subscription.extension = False
            subscription.save()
            if request.method == 'DELETE':
                # DELETE: Вернуть "204" "Автоматическое продление отключено"
                return Response(
                    data='Автоматическое продление отключено.',
                    status=status.HTTP_204_NO_CONTENT
                )
        if request.method == 'DELETE':
            # DELETE: Вернуть "204" "Автоматическое продление отключено"
            return Response(
                data='Автоматическое продление уже отключено.',
                status=status.HTTP_400_BAD_REQUEST
            )
        # PUT: Создать запись со статусом "ожидает оплаты".
        Payment.objects.create(
            rate=rate,
            price=rate.price,
        )
        # date_start = subscription.date_end + datetime.timedelta(days=1)
        # date_end = date_start + datetime.timedelta(days=rate.duration)
        # Subscription.objects.create(
        #     user=user,
        #     rate=rate,
        #     date_start=date_start,
        #     date_end=date_end
        # )
        # Создать задачу на автоматическое продление подписки
        # в день окончания предыдущей.
        return Response(
            data='Тариф подписки обновлен.',
            status=status.HTTP_201_CREATED
        )
        # paginate = self.paginate_queryset(following)
        # serializer = SubscriptionsSerializer(
        #     data=paginate,
        #     many=True,
        #     context={
        #         'request': request
        #     }
        # )
        # serializer.is_valid()
        # return self.get_paginated_response(serializer.data)
