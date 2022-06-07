from rest_framework import serializers
from.models import Student,Teacher
from django.contrib.auth.models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model ='Student'
        fields ='__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model ='Teacher'
        fields ='__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User()
        user.set_password(validated_data['password'])
        validated_data['password'] = user.password
        return super().create(validated_data)


# Serializer for Groups' user
class GroupUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'username', 'email', 'password', 'groups')
        extra_kwargs = {
            'password': {'write_only': True},
        }