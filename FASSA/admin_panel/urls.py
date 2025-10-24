from django.urls import path
from .views import CourseListCreateView, CourseDetailView, TimetableListCreateView, TimetableDetailView

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='admin-courses-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='admin-course-detail'),
    path('timetables/', TimetableListCreateView.as_view(), name='admin-timetables-list-create'),
    path('timetables/<int:pk>/', TimetableDetailView.as_view(), name='admin-timetable-detail'),
]
