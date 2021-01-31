from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class CreateQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    number_of_questions = models.IntegerField()
    category = models.CharField(max_length=64)
    difficulty = models.CharField(max_length=64)
    type_of_question = models.CharField(max_length=64)


    def __str__(self):
        return f"{self.user}, {self.number_of_questions} {self. category}, {self.difficulty}, {self.type_of_question}"

class Stud_Ans(models.Model):
    qna = models.JSONField(null=True)
    stud_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.stud_user}, {self.qna}"