from django import forms 
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="password" , widget=forms.PasswordInput)
    password2 = forms.CharField(label="password2" , widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'email']


    def check_password(self):
        cd = self.cleaned_data

        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password s not match.')
        
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name' , 'email' , 'last_name']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("the email is already exists")
        return data
    


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age' , 'image']

    