from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_quiz", views.create_quiz, name="create_quiz"),
    path("record", views.record, name="record"),
    path("quiz_page/<int:id>", views.quiz_page, name="quiz_page")
]
