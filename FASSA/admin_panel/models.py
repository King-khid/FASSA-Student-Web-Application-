from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    program = models.CharField(max_length=120, blank=True)
    level = models.CharField(max_length=20, blank=True)
    semester = models.CharField(max_length=10, blank=True)
    lecturer = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.code} — {self.title}"


class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.course.code} | {self.day_of_week} {self.start_time}-{self.end_time}"
