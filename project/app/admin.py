from django.contrib import admin
from .models import (
    Course,
    UserCourse,
    CourseMaterial,
    Homework,
    HomeworkSubmission,
    Test,
    TestQuestion,
    TestAttempt,
    TestTries,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "info")
    search_fields = ("name", "subject")
    list_filter = ("subject",)


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "status", "grade")
    list_filter = ("status",)


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    search_fields = ("title", "course__name")


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "max_score")
    search_fields = ("title", "course__name")


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "homework", "submission_date", "score", "attempts")
    search_fields = ("user__username", "homework__title")
    list_filter = ("submission_date",)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "duration")
    search_fields = ("title", "course__name")


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ("test", "question_text")
    search_fields = ("test__title", "question_text")


@admin.register(TestTries)
class TestTriesAdmin(admin.ModelAdmin):
    list_display = ("question", "user", "score", "attempts")
    search_fields = ("user__username", "question__question_text")


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "test", "start_time", "end_time", "score")
    search_fields = ("user__username", "test__title")
    list_filter = ("start_time", "end_time")
