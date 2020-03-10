from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from users.models import User, Profile

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
    #Phone
    phone_regex = RegexValidator(
		regex=r'\+?1?\d{9,15}$',
		message="Phone number debe ser de 10 numeros"
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    password = serializers.CharField(min_length=8,max_length=64)
    password_confirmation = serializers.CharField(min_length=8,max_length=64)

    first_name = serializers.CharField(min_length=2,max_length=30)
    last_name = serializers.CharField(min_length=2,max_length=30)

    def validate (self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Password do not match')
        password_validation.validate_password(passwd)
        return data

    def create(self,data):
        data.pop('password_confirmation')
        user = User.objects.create_user(is_verified=False, **data)
        profile = Profile.objects.create(user=user)
        return user

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