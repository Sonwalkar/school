from django.contrib import admin
from .models import User, CreateQuiz, Stud_Ans

# Register your models here.
admin.site.register(User)
admin.site.register(CreateQuiz)
admin.site.register(Stud_Ans)
