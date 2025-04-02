from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .models import *
from django.contrib.auth.models import User







class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email','password']


from django import forms

class StudentLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Please enter a valid email address.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# class SignupForm(UserCreationForm):
#     profileName = forms.CharField(max_length=255)
#     email=forms.EmailField(required=False)
#     password = forms.CharField(widget=forms.PasswordInput)
#     gender = forms.ChoiceField(choices=[('female', 'Female'), ('male', 'Male'), ('non_binary', 'Non-binary')], required=False)
#     date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)))
#     accept_terms = forms.BooleanField()

#     class Meta:
#         model = User
#         fields = ['profileName', 'email', 'password', 'gender', 'date_of_birth', 'accept_terms']
    


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     accept_terms = forms.BooleanField(required=True)
    
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'placeholder': 'Your username',
            'help_text': 'This will be your public profile name'
        }),
        required=True
    )
    
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@gmail.com',
            'value': 'sh@gmail.com'  # يمكن إزالته في الإنتاج
        }),
        required=True
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Use 8 or more characters with a mix of letters, numbers & symbols'
        }),
        required=True
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(),
        required=True
    )
    
    # GENDER_CHOICES = [
    #     ('F', 'Female'),
    #     ('M', 'Male'),
    #     ('NB', 'Non-binary'),
    # ]
    
    # gender = forms.ChoiceField(
    #     label='Gender (optional)',
    #     choices=GENDER_CHOICES,
    #     widget=forms.RadioSelect,
    #     required=False
    # )
    
    # birth_month = forms.ChoiceField(
    #     label='Month',
    #     choices=[(i, i) for i in range(1, 13)],
    #     required=False
    # )
    
    # birth_date = forms.ChoiceField(
    #     label='Date',
    #     choices=[(i, i) for i in range(1, 32)],
    #     required=False
    # )
    
    # birth_year = forms.ChoiceField(
    #     label='Year',
    #     choices=[(i, i) for i in range(1900, 2023)],
    #     required=False
    # )
    
    accept_terms = forms.BooleanField(
        label='Accept Terms of use and Privacy Policy',
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email



# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     accept_terms = forms.BooleanField(required=True)
#     password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
#     password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
#     class Meta:
#         model = User
#         fields = ('email', 'password1', 'password2')


##here
# class StudentProfileForm(forms.ModelForm):

#     # user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)
#     # student_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
#     # courses = models.ManyToManyField('Course', blank=True)
#     # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
#     # academic_level = models.CharField(max_length=50, blank=True)
#     # major = models.CharField(max_length=100, blank=True)
#     # gender = models.CharField(max_length=10, blank=True)
#     # date_of_birth = models.DateField(null=True, blank=True)
    
#     class Meta:
#         model = StudentProfile
#         model = StudentProfile
#         exclude = ['user']
    
#         # fields = [ 'university',' profile_picture ', 'academic_level','major']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user', 'student_id']  # استبعاد student_id لأنه يتم إنشاؤه تلقائيًا


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    # additionalll
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError("A post with this title already exists.")
        return title
    

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']



