from django.db import models
import os
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from django.core.files.storage import FileSystemStorage
from TeachersDirectory import settings


SUBJECTS = (('computerscience', 'Computer science'),
            ('physics', 'Physics'),
            ('mathematics', 'Mathematics'),
            ('history', 'History'),
            ('geography', 'Geography'),
            ('biology', 'Biology'),
            ('chemistry', 'Chemistry'),
            ('english', 'English'),
            ('arabic', 'Arabic'))


def get_image_path(instance, filename):
    return os.path.join('media', 'teachers', str(instance.id), filename)


fs = FileSystemStorage(location=settings.MEDIA_ROOT)


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(storage=fs)
    email_address = models.EmailField(max_length=254, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    room_number = models.CharField(max_length=10)
    subjects = MultiSelectField(choices=SUBJECTS,
                                max_choices=5)
