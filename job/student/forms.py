from django import forms

from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name','email',"phone", "address","qualification","college","cgpa","experience",'resume']

resume = forms.FileField()


class SignupForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True)



