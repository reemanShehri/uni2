from venv import logger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, StudentProfileForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('complete_profile')  # استبدل 'home' بصفحة التحويل بعد التسجيل
    else:
        form = SignUpForm()
    
    return render(request, 'pages/signup.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             # إنشاء مستخدم جديد
#             user = form.save(commit=False)
#             user.username = form.cleaned_data['email']  # تعيين اسم المستخدم كالإيميل
#             user.set_password(form.cleaned_data['password1'])  # تعيين كلمة المرور
#             user.save()
            
#             logger.debug(f"New user created: {user.email}")
            
#             # تسجيل المستخدم تلقائيًا بعد الإنشاء
#             login(request, user)
#             return redirect('complete_profile')  # إعادة التوجيه إلى لوحة التحكم
#         else:
#             logger.warning(f"Form validation errors: {form.errors}")
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = SignUpForm()
    
#     return render(request, 'pages/signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from .forms import StudentProfileForm  # تأكد من استيراد الفورم

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from .forms import StudentProfileForm  # تأكد من استيراد الفورم





@login_required
def complete_profile(request):

    if StudentProfile.objects.filter(user=request.user).exists():
        return redirect('dashboard')  # إذا كان لديه ملف شخصي، انتقل مباشرةً للداشبورد

    if request.method == 'POST':
        print("🔹 تم استقبال طلب POST")
        form = StudentProfileForm(request.POST, request.FILES)
        print("🔹 محتوى request.POST:", request.POST)
        print("🔹 محتوى request.FILES:", request.FILES)

        if form.is_valid():
            print("✅ النموذج صالح وسيتم حفظ البيانات")
            profile = form.save(commit=False)
            profile.user = request.user  # تعيين المستخدم الحالي للملف الشخصي
            if not profile.student_id:  # التأكد من أن الطالب لديه ID قبل الحفظ
              profile.student_id = generate_student_id()
            
            profile.save()
            form.save_m2m()  # حفظ علاقات ManyToMany

            return redirect('dashboard')  # تحويل المستخدم إلى لوحة التحكم
        
        
        else:
            print("❌ النموذج غير صالح، الأخطاء:")
            print(form.errors)

    else:
        form = StudentProfileForm()

    return render(request, 'pages/completeProfile.html', {'form': form})






from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  # توجيه المستخدم عند نجاح تسجيل الدخول
        else:
            return render(request, 'pages/login.html', {
                'form': StudentLoginForm(),
                'error': 'Invalid email or password.'
            })
    else:
        return render(request, 'pages/login.html', {'form': StudentLoginForm()})




import logging
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

# إعداد نظام تسجيل الأخطاء
logger = logging.getLogger(__name__)

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
            
#             # طباعة البيانات المُدخلة للتأكد من صحتها
#             logger.debug(f"Email entered: {email}, Password entered: {password}")

#             user = authenticate(request, username=email, password=password)
            
#             if user is not None:
#                 logger.debug("User authenticated successfully.")
#                 login(request, user)
#                 return redirect('dashboard')
#             else:
#                 logger.warning("Authentication failed. Invalid email or password.")
#                 messages.error(request, 'Invalid email or password.')
#         else:
#             logger.warning("Form validation failed. Errors: %s", form.errors)
#     else:
#         form = LoginForm()
    
#     return render(request, 'pages/login.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            logger.debug(f"Email entered: {email}, Password entered: {password}")

            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    logger.debug("User authenticated successfully.")
                    return redirect('dashboard')
                else:
                    logger.warning("Authentication failed. Invalid email or password.")
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                logger.warning("User with this email does not exist.")
                messages.error(request, 'Invalid email or password.')
        else:
            logger.warning("Form validation failed. Errors: %s", form.errors)
    else:
        form = LoginForm()
    
    return render(request, 'pages/login.html', {'form': form})

@login_required
def logout(request):
    logout(request)
    return redirect('home')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from .forms import StudentProfileForm  # تأكد من تعريف الفورم



@login_required
def dashboard(request):

 
    # profile = StudentProfile.objects.get(user=request.user)
    # return render(request, 'pages/Dashboard.html', {'profile': profile})

    try:
        student = StudentProfile.objects.get(user=request.user)
        courses = student.courses.all()
        boards = Board.objects.filter(course__in=courses)
        posts = Post.objects.filter(board__in=boards)
        
    except StudentProfile.DoesNotExist:
        student = None
        courses = []
        boards = []
        posts = []
    
    # معالجة نموذج الحفظ
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("dashboard")  # إعادة التوجيه بعد الحفظ
    
    else:
        form = StudentProfileForm(instance=student)
    

    print(student.profile_picture)

    # عرض القالب مع القيم سواء كانت موجودة أو فارغة
    return render(request, 'pages/Dashboard.html', {
        'student': student,
        'courses': courses,
        'boards': boards,
        'posts': posts,
        'form': form,  # تمرير النموذج للقالب
    })


@login_required
def create_post(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = StudentProfile.objects.get(user=request.user)
            post.board = board
            post.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form, 'board': board})

@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    posts = Post.objects.filter(board=board)
    return render(request, 'board_detail.html', {'board': board, 'posts': posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = Reply.objects.filter(post=post)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = StudentProfile.objects.get(user=request.user)
            reply.post = post
            reply.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = ReplyForm()
    return render(request, 'Board.html', {'post': post, 'replies': replies, 'form': form})

@login_required
def create_announcement(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.board = board
            announcement.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = AnnouncementForm()
    return render(request, 'create_announcement.html', {'form': form, 'board': board})





def search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        courses = Course.objects.filter(name__icontains=query)
    else:
        posts = Post.objects.all()
        courses = Course.objects.all()
    return render(request, 'search_results.html', {'posts': posts, 'courses': courses, 'query': query})



@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user.student)
    notification.is_read = True
    notification.save()
    return redirect('dashboard')




def student_detail(request, id):
     student = StudentProfile.objects.get(pk=id)  # Fetch the student using the ID
     return render(request, 'pages/student_detail.html', {'student': student})
