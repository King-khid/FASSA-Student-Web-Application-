from rest_framework import generics, permissions
from .models import Course, Timetable
from .serializers import CourseSerializer, TimetableSerializer
from accounts.permissions import IsAdmin

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all().order_by('code')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class TimetableListCreateView(generics.ListCreateAPIView):
    queryset = Timetable.objects.all().order_by('course__code', 'day_of_week', 'start_time')
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class TimetableDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
