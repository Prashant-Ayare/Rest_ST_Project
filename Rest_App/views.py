from django.shortcuts import render
from.serializers import StudentSerializer,TeacherSerializer
from.models import*
from rest_framework import viewsets

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = TeacherSerializer


from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .serializers import GroupUserSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



# Sign Up API to register a normal user who doesn't belong to any group
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# Defined 3 user levels: 1. Super-admin, 2. Teacher, 3. Student (By using internal Django Groups)


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None

    # POST request to add the new user to the database
    # Student  is unable to add anyone to the database
    # Teacher  is able to add Students to the database
    # Super-Admin (Group no 1) is able to add anyone in the database
    def post(self, request):
        try:
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name  # requesting user's group name
                condition01 = (group == "Super-admin")
                condition02 = ((group == "Teacher") and (request.data['groups'] == [3]))
                if condition01 or condition02:
                    user = request.data
                    # encrypting password with sha_256 algorithm
                    user['password'] = make_password(user['password'])
                    serializer = GroupUserSerializer(data=user)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    err_message = {'status': 401, 'error_message': "user can't add user to same level"}
                    return Response(status=status.HTTP_401_UNAUTHORIZED, data=err_message)
            else:
                err_message = {'status': 401, 'error_message': "user has not access admin/super user ."}
                return Response(status=status.HTTP_401_UNAUTHORIZED, data=err_message)
        except Exception as ex:
            return Response(ex.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# GET request to list users
# Student (Group no 3) is able to list his information from the database
# Teacher (Group no 2) is able to list Students' information from the database
# Super-admin (Group no 1) is able to list anyone's information from the database
    def get(self, request):
        try:
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == "Super-admin":
                    users = User.objects.filter(Q(groups=1) | Q(groups=2) | Q(groups=3))
                    serializer = GroupUserSerializer(users, many=True)
                elif group == "Teacher":
                    users = User.objects.filter(groups=3)
                    serializer = GroupUserSerializer(users, many=True)
                elif group == "Student":
                    users = User.objects.get(id=request.user.id)
                    serializer = GroupUserSerializer(users)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

