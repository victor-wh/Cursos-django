from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone, timesince
from django.conf import settings

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from users.models import User, Profile

import jwt
from datetime import timedelta

class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,max_length=64)

    def validate(self,data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales no validas')
        if not user.is_verified:
            raise serializers.ValidationError('Cuenta no activada aun')
        self.context['user']=user
        return data

    def create (self,data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # Phone sintaxis validacion
    phone_regex = RegexValidator(
		regex=r'\+?1?\d{9,15}$',
		message="Phone number debe ser de 10 numeros"
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    password = serializers.CharField(min_length=8,max_length=64)
    password_confirmation = serializers.CharField(min_length=8,max_length=64)

    first_name = serializers.CharField(min_length=2,max_length=30)
    last_name = serializers.CharField(min_length=2,max_length=30)
    # Verificar qu los campos han sido completados correctamente
    def validate (self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Password do not match')
        password_validation.validate_password(passwd)
        return data
    # Cuando se genere un nuevo usuario
    def create(self,data):
        data.pop('password_confirmation')
        user = User.objects.create_user(is_verified=False, **data)
        profile = Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user
    # Enviar confirmacion de email
    def send_confirmation_email(self, user):
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
        from_email = 'victor.wisphub@gmail.com>'
        to = 'victor.wisphub@gmail.com'
        text_content = 'This is an important message.'
        html_content = '<p>This is your token <strong>'+ verification_token +'</strong> message.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print('sending email')
    
    def gen_verification_token(self, user):
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': exp_date,
            'type':'email_confirmation',
        }
        token = jwt.encode(payload,settings.SECRET_KEY, algorithm='HS256')
        return token.decode()

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )

class AccountVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self,data):
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('link de verificacion ha expirado')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid Token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid Token - email')
        self.context['payload'] = payload
        return data

    def save(self):
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()