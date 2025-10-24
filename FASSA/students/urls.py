from django.urls import path
from .views import AvailableCoursesView, RegisterCourseView, MyCoursesView, PersonalTimetableView

urlpatterns = [
    path('courses/', AvailableCoursesView.as_view(), name='available-courses'),
    path('register-course/', RegisterCourseView.as_view(), name='register-course'),
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('timetable/', PersonalTimetableView.as_view(), name='personal-timetable'),
]
