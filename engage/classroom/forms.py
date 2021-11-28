from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

class assignmentCreationForm(ModelForm):
    class Meta:
        model= Assignment
        fields="__all__"


class courseCreationForm(ModelForm):
    class Meta:
        model= Course
        fields="__all__"

class assignmentSubmissionForm(ModelForm):
    class Meta:
        model= AssignmentSubmission
        fields="__all__"

class createUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2','groups']