from basic_app.models import UserProfileInfo
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model=User
        fields=('username','email','password')
    verify_password=forms.CharField(widget=forms.PasswordInput,required=True)
    

    def clean(self):
        all_clean_data=super().clean()
        
        p=all_clean_data['password']
        v_p=all_clean_data['verify_password']
        if p!=v_p:
            raise forms.ValidationError('PASSWORD IS NOT THE SAME')
    
class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model=UserProfileInfo
        fields=('portfolio_site','profile_pic')