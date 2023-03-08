from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .models import Course, Student, Result


def home(request):
    return render(request, 'mock_exam/student_home.html')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('student-dashboard')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
    return render(request, 'mock_exam/register.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('student-dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('student-dashboard')
            else:
                messages.info(request, 'username or password is incorrect')
    return render(request, 'mock_exam/login.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def student_dashboard(request):
    total_course = Course.objects.all().count()
    context = {
        'total_course': total_course,
    }
    return render(request, 'mock_exam/student_dashboard.html', context)


@login_required(login_url='login')
def student_exam_view(request):
    courses = Course.objects.all()
    return render(request, 'mock_exam/student_exam.html', {'courses': courses})


@login_required(login_url='login')
def take_exam_view(request, pk):
    course = Course.objects.get(id=pk)
    total_question = course.question_number
    total_marks = course.total_marks

    context = {
        'course': course,
        'total_questions': total_question,
        'total_marks': total_marks,
    }
    return render(request, 'mock_exam/take_exam.html', context)


@login_required(login_url='login')
def google_exam_view(request, pk):
    course = Course.objects.get(id=pk)
    Embed_HTML = course.exam_link
    if request.method == 'POST':
        pass
    context = {
        'course': course,
        'Embed_HTML': Embed_HTML,
    }
    return render(request, 'mock_exam/live_exam.html', context)


@login_required(login_url='login')
def student_marks_view(request):
    courses = Course.objects.all()
    return render(request, 'mock_exam/student_marks.html', {'courses': courses})


@login_required(login_url='login')
def check_marks_view(request, pk):
    course = Course.objects.get(id=pk)
    student = Student.objects.get(user_id=request.user.id)
    results = Result.objects.all().filter(exam=course).filter(student=student)
    return render(request, 'mock_exam/check_marks.html', {'results': results})
