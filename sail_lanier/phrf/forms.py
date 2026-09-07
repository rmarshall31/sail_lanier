from django import forms
from django_recaptcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField()
