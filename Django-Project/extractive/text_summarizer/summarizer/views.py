from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .handle import handle_text, handle_upload
from .models import Text

from .forms import CreateUserForm


# Create your views here.


def home(request):
    # messages.success(request, 'Welcome to Summarizer Home')
    return render(request, 'summarizer/student_home.html')


@login_required(login_url='login')
def after_login(request):
    return render(request, 'summarizer/student_base.html')


@login_required(login_url='login')
def text_input(request):
    return render(request, 'summarizer/text_input.html')


@login_required(login_url='login')
def file_input(request):
    return render(request, 'summarizer/file_input.html')


@login_required(login_url='login')
def text_output(request):
    return handle_text(request)


@login_required(login_url='login')
def file_output(request):
    return handle_upload(request)


@login_required(login_url='login')
def download_text_file(request):
    text_object = Text.objects.last()
    text = text_object.summary_output
    username = request.user.username

    # Create the HttpResponse object with the content as a text file
    response = HttpResponse(text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename= "{username}_summary.txt"'
    return response


def register_page(request):
    if request.user.is_authenticated:
        return redirect('after_login')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                # messages.success(request, 'Your profile has been registered')
                return redirect('login')
    # context = {'form': form}
    return render(request, 'summarizer/register1.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('after_login')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('after_login')
            else:
                messages.info(request, 'username or password is incorrect')
    return render(request, 'summarizer/login.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')

