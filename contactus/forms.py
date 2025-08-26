# from django import forms
# from .models import Contact

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['name', 'email', 'subject', 'message']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
#             'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
#             'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
#         }

from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Full Name',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Email',
                'required': 'required'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Subject',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Message',
                'rows': 5,
                'required': 'required'
            }),
        }
