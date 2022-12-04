from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer, ChangePasswordSerializer

User = get_user_model()


class RegisterApiView(APIView):
    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Вам отправлено письмо активации'}, status=status.HTTP_201_CREATED)


class ActivateApiView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Успешно активировано!'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'Неверный код активации'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response({'msg': 'Пароль успешно изменен'})

