from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm, Do_DZ, DoTest, Search
from .models import (
    Course,
    UserCourse,
    CourseMaterial,
    Test,
    Homework,
    HomeworkSubmission,
    TestAttempt,
    TestQuestion,
    TestTries,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.contrib import messages  # Для вывода сообщений пользователю


@login_required
def home_view(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def active_courses_view(request):
    active_courses = UserCourse.objects.filter(
        user=request.user, status="active"
    ).select_related("course")
    return render(request, "active_courses.html", {"active_courses": active_courses})


@login_required
def completed_courses_view(request):
    completed_courses = UserCourse.objects.filter(
        user=request.user, status="completed"
    ).select_related("course")
    return render(
        request, "completed_courses.html", {"completed_courses": completed_courses}
    )


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    materials = CourseMaterial.objects.filter(course=course)
    tests = Test.objects.filter(course=course)
    tasks = Homework.objects.filter(course=course)

    user_course, created = UserCourse.objects.get_or_create(
        user=request.user, course=course
    )

    return render(
        request,
        "course_detail.html",
        {
            "course": course,
            "materials": materials,
            "tests": tests,
            "tasks": tasks,
            "user_course": user_course,
        },
    )


@login_required
def course_results(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user_course = get_object_or_404(UserCourse, user=request.user, course=course)

    # Собираем все домашние задания и их результаты
    homework_submissions = HomeworkSubmission.objects.filter(
        homework__course=course, user=request.user
    ).select_related("homework")
    homework_submissions_dict = {
        submission.homework.id: submission for submission in homework_submissions
    }

    # Собираем все тесты и их результаты
    test_attempts = TestAttempt.objects.filter(
        test__course=course, user=request.user
    ).select_related("test")
    test_attempts_dict = {attempt.test.id: attempt for attempt in test_attempts}

    context = {
        "course": course,
        "user_course": user_course,
        "homework_submissions": homework_submissions_dict,
        "test_attempts": test_attempts_dict,
    }
    return render(request, "course_results.html", context)


@login_required
def course_completed(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "course_completed.html", {"course": course})


@login_required
def material_show(request, pk):
    material = get_object_or_404(CourseMaterial, pk=pk)
    return render(request, "material.html", {"material": material})


@login_required
def do_task(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    obj, created = HomeworkSubmission.objects.get_or_create(
        homework=homework,
        user=request.user,
        defaults={"attempts": 0, "score": homework.max_score},
    )
    if request.method == "POST":
        form = Do_DZ(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data["do_dz"]
            obj.attempts += 1
            if user_answer.strip().lower() == homework.answer.strip().lower():
                obj.save()
                update_course_completion_status(request.user, homework.course)
                return redirect("dz_completed", pk=homework.pk)
            else:
                obj.score -= 1
                if obj.score < 0:
                    obj.score = 0
                obj.save()
    else:
        form = Do_DZ()
    return render(
        request, "do_dz.html", {"form": form, "homework": homework, "obj": obj}
    )


@login_required
def dz_completed(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    obj = HomeworkSubmission.objects.filter(
        homework=homework, user=request.user
    ).first()
    update_course_completion_status(request.user, homework.course)
    user_course = UserCourse.objects.filter(
        user=request.user, course=homework.course
    ).first()
    if user_course.status == "completed":
        return redirect("course_completed", course_id=homework.course.id)
    return render(
        request,
        "dz_completed.html",
        {"homework": homework, "obj": obj, "user_course": user_course},
    )


@login_required
def do_test(request, test_id, question_number):
    test = get_object_or_404(Test, pk=test_id)
    questions = TestQuestion.objects.filter(test=test).order_by("id")
    total_questions = questions.count()

    if question_number > total_questions or question_number < 1:
        return redirect("test", test_id=test_id, question_number=1)

    question = questions[question_number - 1]

    obj, created = TestTries.objects.get_or_create(
        question=question,
        user=request.user,
        defaults={"score": question.max_score, "attempts": 0},
    )
    if request.method == "POST":
        form = DoTest(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data["do_test"]
            obj.attempts += 1
            if user_answer.strip().lower() == question.correct_answer.strip().lower():
                obj.save()
                if question_number < total_questions:
                    return redirect(
                        "test", test_id=test_id, question_number=question_number + 1
                    )
                else:
                    return redirect("end_test", pk=test_id)
            else:
                obj.score -= 1
                if obj.score < 0:
                    obj.score = 0
                obj.save()
    else:
        form = DoTest()

    prev_question = question_number - 1 if question_number > 1 else None
    next_question = question_number + 1 if question_number < total_questions else None

    return render(
        request,
        "test.html",
        {
            "form": form,
            "test": test,
            "question": question,
            "prev_question": prev_question,
            "next_question": next_question,
            "question_number": question_number,
            "total_questions": total_questions,
        },
    )


@login_required
def end_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    total_score = (
        TestTries.objects.filter(question__test__pk=pk, user=request.user).aggregate(
            total=Sum("score")
        )["total"]
        or 0
    )
    result, created = TestAttempt.objects.get_or_create(
        test=test, user=request.user, defaults={"score": total_score}
    )
    if not created:
        result.score = total_score
        result.save()
    update_course_completion_status(request.user, test.course)
    user_course = UserCourse.objects.filter(
        user=request.user, course=test.course
    ).first()
    if user_course.status == "completed":
        return redirect("course_completed", course_id=test.course.id)
    return render(
        request,
        "end_test.html",
        {"total_score": total_score, "test": test, "user_course": user_course},
    )


@login_required
def test_completed(request, pk):
    test = get_object_or_404(Test, pk=pk)
    questions = TestQuestion.objects.filter(test=test)
    return render(
        request, "test_completed.html", {"test": test, "questions": questions}
    )


@login_required
def search(request):
    courses = None
    active_course_ids = UserCourse.objects.filter(
        user=request.user, status="active"
    ).values_list("course_id", flat=True)
    completed_course_ids = UserCourse.objects.filter(
        user=request.user, status="completed"
    ).values_list("course_id", flat=True)
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            answer = form.cleaned_data["search"]
            courses = Course.objects.filter(
                Q(name__icontains=answer) | Q(subject__icontains=answer)
            )
    else:
        form = Search()
    return render(
        request,
        "search.html",
        {
            "form": form,
            "courses": courses,
            "active_course_ids": active_course_ids,
            "completed_course_ids": completed_course_ids,
        },
    )


@login_required
def add_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Проверяем, уже добавлен ли курс в активные или завершенные
    user_course, created = UserCourse.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={"status": "active"},  # Не устанавливаем grade при создании
    )
    if not created:
        if user_course.status == "active":
            messages.info(request, "Этот курс уже добавлен в активные.")
        elif user_course.status == "completed":
            # Переключаем статус на active и сбрасываем оценку
            user_course.status = "active"
            user_course.grade = None  # Сбрасываем оценку
            user_course.save()
            messages.success(
                request, f"Курс '{course.name}' снова добавлен в активные."
            )
    else:
        messages.success(request, f"Курс '{course.name}' добавлен в активные.")

    return redirect("search")


def update_course_completion_status(user, course):
    all_homeworks = Homework.objects.filter(course=course)
    all_tests = Test.objects.filter(course=course)

    total_homeworks = all_homeworks.count()
    total_tests = all_tests.count()

    completed_homeworks = HomeworkSubmission.objects.filter(
        user=user, homework__in=all_homeworks
    ).count()

    completed_tests = TestAttempt.objects.filter(user=user, test__in=all_tests).count()

    if total_homeworks == 0 and total_tests == 0:
        return

    if completed_homeworks == total_homeworks and completed_tests == total_tests:
        total_homework_score = (
            HomeworkSubmission.objects.filter(
                user=user, homework__in=all_homeworks
            ).aggregate(total=Sum("score"))["total"]
            or 0
        )

        total_test_score = (
            TestAttempt.objects.filter(user=user, test__in=all_tests).aggregate(
                total=Sum("score")
            )["total"]
            or 0
        )

        total_possible_homework_score = (
            all_homeworks.aggregate(total=Sum("max_score"))["total"] or 0
        )

        total_possible_test_score = (
            all_tests.aggregate(total=Sum("max_score"))["total"] or 0
        )

        total_possible_score = total_possible_homework_score + total_possible_test_score

        total_score = total_homework_score + total_test_score

        if total_possible_score > 0:
            grade = (total_score / total_possible_score) * 10  # Оценка из 10
        else:
            grade = 0

        user_course, created = UserCourse.objects.get_or_create(
            user=user, course=course, defaults={"status": "completed", "grade": grade}
        )
        if not created:
            user_course.status = "completed"
            user_course.grade = grade
            user_course.save()
