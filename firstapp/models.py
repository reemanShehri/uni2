import uuid
import django
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.models import AbstractUser

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.apps import apps




# class CustomUser(AbstractUser):  # استخدم الحرف الكبير "C"
#     email = models.EmailField(unique=True)  # بريد إلكتروني فريد
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []



MAJOR_CHOICES = [
    ('CS', 'Computer Science'),
    ('EE', 'Electrical Engineering'),
    ('ME', 'Mechanical Engineering'),
    ('CE', 'Civil Engineering'),
    ('SE', 'Software Engineering'),
    ('BBA', 'Business Administration'),
    ('ACC', 'Accounting'),
    ('FIN', 'Finance'),
    ('MKT', 'Marketing'),
    ('ECO', 'Economics'),
    ('PSY', 'Psychology'),
    ('SOC', 'Sociology'),
    ('BIO', 'Biology'),
    ('CHEM', 'Chemistry'),
    ('PHYS', 'Physics'),
    ('MATH', 'Mathematics'),
    ('STAT', 'Statistics'),
    ('MED', 'Medicine'),
    ('PHARM', 'Pharmacy'),
    ('LAW', 'Law'),
    ('POL', 'Political Science'),
    ('ENG', 'English Literature'),
    ('ART', 'Fine Arts'),
    ('ARCH', 'Architecture'),
    ('EDU', 'Education'),
    ('HIST', 'History'),
    ('GEO', 'Geography'),
    ('IT', 'Information Technology'),
    ('CSE', "Computer's Systemd Engineering") ,
     ('al',"arabic language") # ✅ Added your requested field
]


def get_default_major():
    major = Major.objects.first()
    return major.id if major else None


# def populate_majors():
#     """إدراج جميع التخصصات داخل جدول Major"""
#     for code, name in MAJOR_CHOICES:
#         Major.objects.get_or_create(name=name)


class Major(models.Model):
    name = models.CharField(max_length=100, unique=True)
    universities = models.ManyToManyField('University', related_name='majors')
    
    def __str__(self):
        return self.name

    
    class Meta:
        db_table = "firstapp_major"


class University(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    established_year = models.IntegerField()

    def __str__(self):
        return self.name






# class Login(models.Model):
#             username = models.CharField(max_length=150, unique=True)
#             password = models.CharField(max_length=128)
#             def str(self):
#    
# 
#              return f"{self.username} - {self.last_login}"




ACADEMIC_LEVEL_CHOICES = [
    ('level 1', 'Level 1'),
    ('level 2', 'Level 2'),
    ('level 3', 'Level 3'),
    ('level 4', 'Level 4'),
]


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    university = models.ForeignKey('University', on_delete=models.CASCADE)   
    major = models.ForeignKey('Major', on_delete=models.CASCADE, default=get_default_major, null=True, blank=True)
    academic_level = models.CharField(max_length=50, choices=ACADEMIC_LEVEL_CHOICES, default='level 1') 
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"







import uuid

def generate_student_id():
    return str(uuid.uuid4())
class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # بدلًا من auth.User
        on_delete=models.CASCADE,
        # related_name="student_profile"
    )    
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey('University', on_delete=models.CASCADE, null=True, blank=True) 
    student_id = models.CharField(max_length=20, unique=True, default=generate_student_id)
    courses = models.ManyToManyField('Course', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    academic_level = models.CharField(max_length=50, blank=True)
    # major = models.ForeignKey('Major', on_delete=models.CASCADE, default=get_default_major)
    major = models.CharField(max_length=100, choices=MAJOR_CHOICES, null=True, blank=True,default=get_default_major)
    gender = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_student = models.BooleanField(default=True, null=True)
    

    def __str__(self):
        return self.user.username 



class Board(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # اسم التصنيف
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # وقت الإنشاء

    def __str__(self):
        return self.name  # يعيد اسم التصنيف لعرضه بسهولة



class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, default=1)  # Remove default=2022
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    def str(self):
        return f"Post by {self.author.username}"
    





class Reply(models.Model):
    content = models.TextField()
    author = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,default=1)  # Remove default=2022
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def str(self):
        return f"Reply by {self.author.user.username} on {self.post.title}"

class Notification(models.Model):
    user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def str(self):
        return self.message


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(default='Default auth', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)
    board = models.ForeignKey(default='Default Board', on_delete=django.db.models.deletion.CASCADE, to='firstapp.board')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def str(self):
        return self.title

class Admin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # بدلًا من auth.User
        on_delete=models.CASCADE
    )    
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)

    def str(self):
        return self.user.username
    


from django.db import models


def get_default_university():
    first_university = University.objects.order_by('id').first()
    return first_university.id if first_university else None  # إرجاع ID إذا وجدت جامعة


class Activity(models.Model):
    title = models.CharField(max_length=200)  # عنوان النشاط
    description = models.TextField()  # وصف النشاط
    category = models.CharField(max_length=100, choices=[('Courses', 'Courses'), ('Events', 'Events')])  # نوع النشاط
    university = models.ForeignKey(University, on_delete=models.CASCADE, default=get_default_university)  # الجامعة المرتبطة بالنشاط
    major_required = models.CharField(max_length=100, blank=True, null=True)  
    start_date = models.DateTimeField()  # تاريخ البدء
    end_date = models.DateTimeField()  # تاريخ الانتهاء
    location = models.CharField(max_length=255, blank=True, null=True)  # الموقع (اختياري)
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء
    updated_at = models.DateTimeField(auto_now=True)  # تاريخ التحديث

    def __str__(self):
        return self.title
