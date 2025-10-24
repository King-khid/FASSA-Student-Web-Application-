from rest_framework import generics, permissions, filters
from admin_panel.models import Course, Timetable
from .models import CourseRegistration
from .serializers import CourseListSerializer, CourseRegistrationSerializer, TimetableEntrySerializer
from accounts.permissions import IsStudent


class AvailableCoursesView(generics.ListAPIView):
    """List all available courses students can register for"""
    queryset = Course.objects.all().order_by('code')
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'code', 'lecturer__name']
    ordering_fields = ['code', 'title']


class RegisterCourseView(generics.CreateAPIView):
    """Register a student for a course"""
    serializer_class = CourseRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]


class MyCoursesView(generics.ListAPIView):
    """List all courses registered by the logged-in student"""
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        regs = CourseRegistration.objects.filter(student=self.request.user)
        return Course.objects.filter(id__in=regs.values_list('course_id', flat=True))


class PersonalTimetableView(generics.ListAPIView):
    """Display student's personalized timetable"""
    serializer_class = TimetableEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        regs = CourseRegistration.objects.filter(student=self.request.user).values_list('course_id', flat=True)
        return Timetable.objects.filter(course_id__in=regs).order_by('day_of_week', 'start_time')
