from rest_framework import serializers
from admin_panel.models import Course, Timetable
from .models import CourseRegistration

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'program', 'level', 'semester', 'lecturer']

class CourseRegistrationSerializer(serializers.ModelSerializer):
    course_detail = CourseListSerializer(source='course', read_only=True)

    class Meta:
        model = CourseRegistration
        fields = ['id', 'course', 'course_detail', 'date_registered']
        read_only_fields = ['date_registered']

    def create(self, validated_data):
        student = self.context['request'].user
        course = validated_data['course']
        obj, created = CourseRegistration.objects.get_or_create(student=student, course=course)
        if not created:
            raise serializers.ValidationError("You are already registered for this course.")
        return obj

class TimetableEntrySerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Timetable
        fields = ['id', 'course', 'course_code', 'course_title', 'day_of_week', 'start_time', 'end_time', 'venue']
