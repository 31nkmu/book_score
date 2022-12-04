from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications.account.send_mail import send_activation_code

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs.pop('password2')
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_activation_code(user.email, code)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6)
    new_password = serializers.CharField(min_length=6)
    new_password_confirm = serializers.CharField(min_length=6)

    def validate(self, attrs):
        p1 = attrs['new_password']
        p2 = attrs['new_password_confirm']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def validate_old_password(self, old_password):
        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError('Старый пароль введен неверно')
        return old_password

    def set_new_password(self):
        password = self.validated_data.get('new_password')
        user = self.context.get('user')
        user.set_password(password)
        user.save()
