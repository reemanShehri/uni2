from django.contrib import admin
from .models import *  # استيراد النموذج

# تسجيل النموذج في واجهة الإدارة
admin.site.register(Post)
admin.site.register(University)
admin.site.register(Tag)
# admin.site.register(Course)


admin.site.register(Board)
admin.site.register(StudentProfile)
admin.site.register(Reply)
admin.site.register(Major)
admin.site.register(Notification)
admin.site.register(Announcement)
admin.site.register(Admin)
admin.site.register(Activity)



class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'major', 'university', 'academic_level')
    fields = ('name', 'major', 'university', 'academic_level', 'description', 'credits')



admin.site.register(Course, CourseAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin



from django.contrib import admin
from .models import Course

# class CourseAdmin(admin.ModelAdmin):
#     filter_horizontal = ('universities', 'major')  # يسمح باختيار أكثر من خيار

# admin.site.register(Course, CourseAdmin)  # يجب تسجيل النموذج وليس الكلاس الإداري فقط



