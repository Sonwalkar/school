from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from .models import User, CreateQuiz, Stud_Ans
import requests

# Create your views here.
def index(request):
    return render(request, "quiz/index.html",{
        "quiz" : CreateQuiz.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "quiz/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "quiz/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "quiz/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "quiz/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "quiz/register.html")


def create_quiz(request):
    if request.method == "POST":
        number_of_questions = request.POST.get("numberOfQuestion")
        category = request.POST.get("category")
        difficulty = request.POST.get("difficulty")
        type_of_question = request.POST.get("type")

        createQ = CreateQuiz(user=request.user, number_of_questions=number_of_questions, category=category, difficulty=difficulty, type_of_question=type_of_question)
        createQ.save()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "quiz/create_quiz.html")


def quiz_page(request, id):
    #shows all the questions randomly on loads
    url = "https://opentdb.com/api.php?amount="
    quiz_details = CreateQuiz.objects.filter(id=id)
    url += str(list(set(quiz_details.values_list("number_of_questions", flat=True)))[0])
    
    if str(list(set(quiz_details.values_list("category", flat=True)))[0]) != 'any':
        url += "&category=" + str(list(set(quiz_details.values_list("category", flat=True)))[0])
    
    if str(list(set(quiz_details.values_list("difficulty", flat=True)))[0]) != "any":
        url += "&difficulty=" + str(list(set(quiz_details.values_list("difficulty", flat=True)))[0])
    
    if str(list(set(quiz_details.values_list("type_of_question", flat=True)))[0]) != "any":
        url += "&type=" + str(list(set(quiz_details.values_list("type_of_question", flat=True)))[0])
    #requests.get('https://opentdb.com/api.php?amount=....').json()
    qnas = requests.get(url).json()
    
    if request.method == "POST":
        if request.POST.get("record") == "record":
            # if user wants to records answers and submit
            rec = Stud_Ans(qna=qnas,stud_user= request.user)
            rec.save()
            return render(request, "quiz/index.html",{
            "quiz" : CreateQuiz.objects.all()
        })
        #if user wants to only submit
        return render(request, "quiz/index.html",{
            "quiz" : CreateQuiz.objects.all()
        })
    
    
    return render(request, "quiz/quiz_page.html",{
        "questions" : qnas,
        "quiz_details" : CreateQuiz.objects.filter(id=id)
    })

def record(request):
# shows all the records the perticular user
    try:
        qnasa = Stud_Ans.objects.get(stud_user= request.user)
        qa = qnasa.qna
        return render(request, "quiz/record.html",{
        "questions" : qa
        })
    except MultipleObjectsReturned:
        qnasa = Stud_Ans.objects.filter(stud_user= request.user).all()
        return render(request, "quiz/record.html",{
        "questions" : qnasa
        })
    except ObjectDoesNotExist:
        return render(request, "quiz/record.html",{
        "questions" : "No records available"
        })