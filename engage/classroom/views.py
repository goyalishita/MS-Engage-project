from typing import Counter
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.

@login_required(login_url='login')
def home(request):
    courses = Course.objects.all()
    print(courses[0])
    context={'courses': courses,
            }
    return render(request,'main.html',context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['teacher'])
def createcourse(request):
    form = courseCreationForm()
    if request.method == 'POST':
        form = courseCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'creation.html',context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['student'])
def submitassignment(request,pk):
    form = assignmentSubmissionForm()
    assignment = Assignment.objects.get(pk=pk)
    print(form)
    if request.method == 'POST':
        form = assignmentSubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={
        'form':form,
        'assignment' : assignment,
    }
    return render(request,'assignmentsubmission.html',context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['teacher'])
def createassignment(request):
    form = assignmentCreationForm()
    if request.method == 'POST':
        form = assignmentCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'creation.html',context)

@login_required(login_url='login')
def viewSubmissions(request, pk):
    assignmentsubmission = AssignmentSubmission.objects.filter(assignment = pk)
    # course = Course.objects.get(pk=pk)
    # print(assignments)
    # courses = Course.objects.all()
    # print(courses[0])
    context={
        'assignmentsubmission': assignmentsubmission,
            }
    return render(request,'viewSubmissions.html',context)

@login_required(login_url='login')
def viewassignments(request, pk):
    assignments = Assignment.objects.filter(course = pk)
    course = Course.objects.get(pk=pk)
    print(assignments)
    # courses = Course.objects.all()
    # print(courses[0])
    context={
        'course':course,
        'assignments': assignments,
            }
    return render(request,'viewassignments.html',context)


@unauthorized_user
def registerPage(request):
    form=createUserForm()
    if request.method=='POST':
        form=createUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=form.cleaned_data.get('groups')
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')
            email=form.cleaned_data.get('email')

            if(group[0] == Group.objects.get(name='student')):
                Student.objects.create(user=user,firstname = firstname, lastname =lastname, studentid=username,email=email)
            else:
                user.is_staff = True
                Teacher.objects.create(user=user,firstname = firstname, lastname =lastname, teacherid=username,email=email)

            messages.success(request,'Account created for '+username)
            return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)

@unauthorized_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is invalid')
    return render(request,'login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')