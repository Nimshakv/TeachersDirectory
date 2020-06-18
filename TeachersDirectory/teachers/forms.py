from .models import Teacher
from django.contrib.auth.forms import UserCreationForm
from django import forms


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher

        SUBJECTS = (('computerscience', 'Computer science'),
                    ('physics', 'Physics'),
                    ('mathematics', 'Mathematics'),
                    ('history', 'History'),
                    ('geography', 'Geography'),
                    ('biology', 'Biology'),
                    ('chemistry', 'Chemistry'),
                    ('english', 'English'),
                    ('arabic', 'Arabic'))
        subjects = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                              choices=SUBJECTS)

        fields = '__all__'