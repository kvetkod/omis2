from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название курса")
    subject = models.CharField(max_length=255, verbose_name="Предмет")
    image = models.ImageField(
        upload_to="course_images/", verbose_name="Фотография", null=True, blank=True
    )
    info = models.TextField(verbose_name="О курсе", null=True, blank=True)

    def __str__(self):
        return self.name


class UserCourse(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        User,
        related_name="user_courses",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        related_name="user_courses",
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="Статус курса",
    )
    grade = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Оценка",
        help_text="Оценка доступна только для завершённых курсов",
    )

    def __str__(self):
        return f"{self.user.username} - {self.course.name} ({self.status})"

    class Meta:
        unique_together = ("user", "course")

    def clean(self):
        if self.status != "completed" and self.grade is not None:
            raise ValidationError(
                "Оценка может быть задана только для завершённых курсов."
            )
        if self.status == "completed" and self.grade is None:
            raise ValidationError("Завершённый курс должен иметь оценку.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class CourseMaterial(models.Model):
    course = models.ForeignKey(
        Course, related_name="materials", on_delete=models.CASCADE, verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название материала")
    content = models.TextField(verbose_name="Содержимое материала")
    video_url = models.URLField(verbose_name="Ссылка на видео", null=True, blank=True)

    def __str__(self):
        return self.title


class Homework(models.Model):
    course = models.ForeignKey(
        Course, related_name="homeworks", on_delete=models.CASCADE, verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название задания")
    description = models.TextField(verbose_name="Описание задания")
    max_score = models.IntegerField(default=10, verbose_name="Максимальная оценка")
    answer = models.TextField(verbose_name="Ответ")

    def __str__(self):
        return self.title


class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(
        Homework,
        related_name="submissions",
        on_delete=models.CASCADE,
        verbose_name="Задание",
    )
    user = models.ForeignKey(
        User,
        related_name="homework_submissions",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    submission_date = models.DateTimeField(default=now, verbose_name="Дата выполнения")
    score = models.IntegerField(verbose_name="Оценка", default=0)
    attempts = models.IntegerField(default=0, verbose_name="Количество попыток")

    def __str__(self):
        return f"{self.user.username} - {self.homework.title}"


class Test(models.Model):
    course = models.ForeignKey(
        Course, related_name="tests", on_delete=models.CASCADE, verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название теста")
    duration = models.DurationField(verbose_name="Длительность теста")
    max_score = models.IntegerField(verbose_name="Макс оценка")

    def __str__(self):
        return self.title


class TestQuestion(models.Model):
    test = models.ForeignKey(
        Test, related_name="questions", on_delete=models.CASCADE, verbose_name="Тест"
    )
    question_text = models.TextField(verbose_name="Текст вопроса")
    correct_answer = models.TextField(verbose_name="Правильный ответ")
    max_score = models.IntegerField(default=2, verbose_name="Максимальная оценка")

    def __str__(self):
        return self.question_text


class TestTries(models.Model):
    question = models.ForeignKey(
        TestQuestion,
        related_name="test_tries",
        on_delete=models.CASCADE,
        verbose_name="Вопрос",
    )
    user = models.ForeignKey(
        User,
        related_name="test_user_tries",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    score = models.IntegerField(verbose_name="Оценка", default=0)
    attempts = models.IntegerField(default=0, verbose_name="Количество попыток")


class TestAttempt(models.Model):
    test = models.ForeignKey(
        Test, related_name="attempts", on_delete=models.CASCADE, verbose_name="Тест"
    )
    user = models.ForeignKey(
        User,
        related_name="test_attempts",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    start_time = models.DateTimeField(default=now, verbose_name="Начало теста")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Конец теста")
    score = models.IntegerField(null=True, blank=True, verbose_name="Оценка")

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"
