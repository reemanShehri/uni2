from django.apps import AppConfig

class FirstAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firstapp'

    def ready(self):
        # للتحقق من أن الدالة تعمل (اختياري)
        print("🚀 ready() is running!")  
        
        # استيراد وتشغيل وظيفة الملء التلقائي
        from firstapp.utils import populate_majors
        populate_majors()
        
        # تسجيل الإشارات (الأهم)
        import firstapp.signals  # تأكد من وجود ملف signals.py