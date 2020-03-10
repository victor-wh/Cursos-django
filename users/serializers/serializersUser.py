from django.contrib.auth import authenticate

from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    pasword = serializers.CharField(min_length=8,max_length=64)

    def validate(self,data):
        user = authenticate(username=['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        return data