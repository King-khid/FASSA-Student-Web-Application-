from rest_framework import serializers
from .models import Course, Timetable

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'program', 'level', 'semester', 'lecturer']

class TimetableSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Timetable
        fields = ['id', 'course', 'course_code', 'course_title', 'day_of_week', 'start_time', 'end_time', 'venue']
