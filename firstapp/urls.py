from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import logout_view
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('Dashboard/', views.dashboard, name='dashboard'),
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    path('board/<int:board_id>/create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('board/<int:board_id>/create_announcement/', views.create_announcement, name='create_announcement'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('complete-profile/Dashboard.html', views.dashboard, name='profile_dashboard'),
    path('student/<int:id>/', views.student_detail, name='student_detail'),
    # path('course/', views.course_selection, name='course'),

    path('major/', views. major_list, name='major'),


     path('course/', views.course_selection, name='course'),
path('courses/register/<int:course_id>/', views.register_course, name='register_course'),

    path('logout/', logout_view, name='logout'),  # تسجيل الخروج التلقائي
#  path('logout/', LogoutView.as_view(), name='logout'),
path('activity/', views.filtered_activities, name='activity'),
path('posts/', views.post_list, name='post_list'),
path('posts/<int:post_id>/', views.post_detail, name='post_detail_view'),
path('create-post/', views.create_post, name='create_post'),
path('posts/<int:post_id>/add-comment/', views.add_comment, name='add_comment'),
path('posts/<int:post_id>/like/', views.like_post, name='like_post'),

]