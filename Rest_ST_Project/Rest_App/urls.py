from rest_framework import routers
from.views import StudentViewSet,TeacherViewSet
from django.urls import path,include
from .views import RegisterView, UserAPIView



router=routers.DefaultRouter()
router.register('r students',StudentViewSet)
router.register('r teachers',TeacherViewSet)

urlpatterns=[
    path('school/',include(router.urls)),
    path('register', RegisterView.as_view()),
    path('manage', UserAPIView.as_view())

]

