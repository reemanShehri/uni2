from venv import logger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

import logging
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
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
   

@login_required
def complete_profile(request):
   
    if StudentProfile.objects.filter(user=request.user).exists():
        return redirect('dashboard')

    if request.method == 'POST':
        print("🔹 تم استقبال طلب POST")
        form = StudentProfileForm(request.POST, request.FILES)

        if form.is_valid():
            print("✅ النموذج صالح وسيتم حفظ البيانات")
            profile = form.save(commit=False)
            profile.user = request.user  

            
            if not profile.student_id:
                profile.student_id = generate_student_id()

            profile.save()
            form.save_m2m()  # حفظ علاقات ManyToMany
            return redirect('dashboard')

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

def login(request,user):
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





logger = logging.getLogger(__name__)



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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from .forms import StudentProfileForm  # تأكد من تعريف الفورم



# @login_required
# def dashboard(request):

#     try:
#         student = StudentProfile.objects.get(user=request.user)
#         courses = student.courses.all()
#         boards = Board.objects.filter(course__in=courses)
#         posts = Post.objects.all().order_by('-created_at')
        
#     except StudentProfile.DoesNotExist:
#         student = None
#         courses = []
#         boards = []
#         posts = []
    
#     # معالجة نموذج الحفظ
#     if request.method == "POST":
#         form = StudentProfileForm(request.POST, request.FILES, instance=student)
#         if form.is_valid():
#             form.save()
#             return redirect("dashboard")  # إعادة التوجيه بعد الحفظ
    
#     else:
#         form = StudentProfileForm(instance=student)
    

#     # print(student.profile_picture)

#     # عرض القالب مع القيم سواء كانت موجودة أو فارغة
#     return render(request, 'pages/Dashboard.html', {
#         'student': student,
#         'courses': courses,
#         'boards': boards,
#         'posts': posts,
#         'form': form,  # تمرير النموذج للقالب
#     })


@login_required
def dashboard(request):
    try:
        student = StudentProfile.objects.get(user=request.user)
        courses = student.courses.all()
        boards = Board.objects.filter(course__in=courses)
        posts = Post.objects.all().order_by('-created_at')
        all_posts = Post.objects.all().order_by('-created_at')  # جميع المنشورات        
        
    except StudentProfile.DoesNotExist:
        student = None
        courses = []
        boards = []
        posts = []
        all_posts = []
    
 
    if request.method == "POST":
     
        if 'post_content' in request.POST:
            post_content = request.POST.get('post_content')
            if post_content:
                Post.objects.create(
                    author=student,
                    content=post_content,
                    university=student.university if student else None
                )
                messages.success(request, 'تم نشر المنشور بنجاح!')
                return redirect("dashboard")
        
     
        elif 'profile_form' in request.POST:
            form = StudentProfileForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'updated successfuly')
                return redirect("dashboard")
    
    else:
        form = StudentProfileForm(instance=student)
 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            action = request.POST.get('action')
            
            if action == 'like':
                post = get_object_or_404(Post, id=post_id)
                if request.user in post.likes.all():
                    post.likes.remove(request.user)
                    return JsonResponse({'status': 'unliked', 'likes_count': post.likes.count()})
                else:
                    post.likes.add(request.user)
                    return JsonResponse({'status': 'liked', 'likes_count': post.likes.count()})
            
            elif action == 'comment':
                post = get_object_or_404(Post, id=post_id)
                comment_content = request.POST.get('comment_content')
                if comment_content:
                    comment = Reply.objects.create(
                        post=post,
                        author=student,
                        content=comment_content
                    )
                    return JsonResponse({
                        'status': 'success',
                        'comment': comment.content,
                        'author': comment.author.username,
                        'created_at': comment.created_at.strftime("%b %d, %Y %I:%M %p")
                    })

    return render(request, 'pages/Dashboard.html', {
        'student': student,
        'courses': courses,
        'boards': boards,
        'user_posts': posts,
        'all_posts': all_posts,
        'form': form,
        'post_form': PostForm(),  # نموذج إنشاء بوست جديد
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


from django.shortcuts import render
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'pages/courses.html', {'courses': courses})



from django.shortcuts import render, redirect
from .models import Course, StudentProfile



def major_list(request):
   
    majors = Major.objects.all()
    return render(request, 'pages/majors.html', {'majors': majors})
@login_required
def course_selection(request):
    student = StudentProfile.objects.get(user=request.user)

    available_courses = Course.objects.filter(
        university=student.university,
        major=student.major,
        academic_level=student.academic_level
    )

    if request.method == "POST":
        selected_courses = request.POST.getlist('courses')  # جلب المساقات المختارة من الطلب
        for course_id in selected_courses:
            course = Course.objects.get(id=course_id)
            student.courses.add(course)  # تسجيل المساق في سجل الطالب
        return redirect('dashboard')  # توجيه الطالب إلى صفحته بعد التسجيل

    return render(request, 'pages/available_courses.html', {'courses': available_courses})








def available_courses(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    university = student.university
    major = student.major

    # جلب المساقات التي تتبع نفس الجامعة ونفس التخصص
    courses = Course.objects.filter(university=university, major=major)

    return render(request, 'pages/available_courses.html', {'courses': courses})



from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.shortcuts import redirect

def register_course(request, course_id):
    student = get_object_or_404(StudentProfile, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    print(f"🚀 Debug: course_id = {course_id}") 
    # التأكد أنه من نفس الجامعة والتخصص (اختياري)
    if course.university == student.university and course.major == student.major:
        student.courses.add(course)
        return redirect('dashboard') 

    return HttpResponseRedirect(reverse('available_courses'))



# from django.contrib.auth import logout
# from django.shortcuts import redirect

# @login_required
# def logout_view(request):
#         logout(request)
#         messages.success(request,"you were logged out..")
#         return redirect('home')





from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)  # تنفيذ عملية تسجيل الخروج
        messages.success(request, "You have been logged out.")
        return redirect('home')  # إعادة توجيه المستخدم إلى الصفحة الرئيسية بعد الخروج
    else:
        # إذا لم تكن الطريقة POST، فسنرفض الوصول للصفحة
        return HttpResponse("Invalid request method.", status=405)

# from django.contrib.auth import logout
# from django.shortcuts import redirect, HttpResponse

# def logout_view(request):
#     if request.user.is_authenticated:  # تأكد من أن المستخدم مسجل الدخول
#         logout(request)
#         return redirect('/')  # إعادة التوجيه للصفحة الرئيسية بعد تسجيل الخروج
#     else:
#         return HttpResponse("User is not authenticated", status=400)  # معالجة المستخدم غير المسجل




from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Activity  # تأكد من استيراد النموذج المناسب


def activity_view(request):
    # جلب البيانات من قاعدة البيانات
    activities = Activity.objects.all()

    # تطبيق الفلترة بناءً على معايير معينة (مثال: تصفية بناءً على الفئة)
    category = request.GET.get('category')  # الحصول على الفئة من الطلب
    if category:
        activities = activities.filter(category=category)

    # تمرير البيانات إلى القالب
    return render(request, 'pages/activity.html', {'activities': activities})



from django.shortcuts import render
from .models import Activity,StudentProfile
from django.core.exceptions import ObjectDoesNotExist


@login_required
def filtered_activities(request):
    # الحصول على بروفايل الطالب أو إنشائه إذا لم يكن موجوداً
    student, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'university': University.objects.first()  # قيمة افتراضية
        }
    )
    
    # جلب البيانات المطلوبة
    activities = Activity.objects.filter(university=student.university)
    courses_taken = student.courses.count()  # عدد الكورسات المسجلة
    active_activities = activities.count()  # عدد الأنشطة الفعلية
    
    # إعداد بيانات الصورة
    profile_image_url = None
    if hasattr(request.user, 'profile') and request.user.profile.image:
        profile_image_url = request.user.profile.image.url
    
    context = {
        'activities': activities,
        'courses_taken': courses_taken,
        'active_activities': active_activities,
        'profile_image_url': profile_image_url,
        'student': student,
    }
    
    return render(request, 'pages/activity.html', context)






@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('dashboard')
    else:
        form = PostForm()
    
    # If we get here, either it's a GET request or form is invalid
    context = {
        'form': form,
    }
    return render(request, 'dashboard.html', context)




def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = Reply.objects.filter(post=post).order_by('created_at')
    return render(request, 'posts/post_detail.html', {'post': post, 'replies': replies})




@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Reply.objects.create(
                post=post,
                author=request.user,
                content=content
            )
    return redirect('dashboard')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('dashboard')
