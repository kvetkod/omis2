from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("course/<int:pk>/", views.course_detail, name="course_detail"),
    path(
        "course_results/<int:course_id>/", views.course_results, name="course_results"
    ),
    path(
        "course_completed/<int:course_id>/",
        views.course_completed,
        name="course_completed",
    ),
    path("active-courses/", views.active_courses_view, name="active_courses"),
    path("completed-courses/", views.completed_courses_view, name="completed_courses"),
    path("material/<int:pk>/", views.material_show, name="material"),
    path("homework/<int:pk>/", views.do_task, name="homework"),
    path("dz_completed/<int:pk>/", views.dz_completed, name="dz_completed"),
    path("test/<int:test_id>/<int:question_number>/", views.do_test, name="test"),
    path("end_test/<int:pk>/", views.end_test, name="end_test"),
    path("test_completed/<int:pk>/", views.test_completed, name="test_completed"),
    path("search/", views.search, name="search"),
    path(
        "add_course/<int:course_id>/", views.add_course, name="add_course"
    ),  # Новый маршрут
]
