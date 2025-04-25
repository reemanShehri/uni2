import os


# 🔧 تأكد من استخدام اسم مجلد الإعدادات (عادةً يكون نفس اسم مجلد المشروع)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UniHubBack.settings')




def populate_majors():
    from firstapp.models import Major
    


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


    """إدراج جميع التخصصات داخل جدول Major"""
    for code, name in MAJOR_CHOICES:
        Major.objects.get_or_create(name=name)




if __name__ == '__main__':
    populate_majors()