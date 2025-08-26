from django import forms
from django.core.validators import RegexValidator
from .models import Coupon
from django.utils import timezone

class ContactDetailsForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Email',
            'required': True
        })
    )
    phone = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be entered in the format: +999999999. Up to 15 digits allowed.'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Phone Number',
            'required': True
        })
    )

class PaymentForm(forms.Form):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect(attrs={'class': 'payment-method-radio'})
    )
    
    card_number = forms.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\d{4}\s\d{4}\s\d{4}\s\d{4}$',
                message='Card number must be in format: 1234 5678 9012 3456'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'id': 'card_number'
        }),
        required=False
    )
    
    card_holder_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name on the Card',
            'id': 'card_holder_name'
        }),
        required=False
    )
    
    expiry_date = forms.CharField(
        max_length=5,
        validators=[
            RegexValidator(
                regex=r'^\d{2}/\d{2}$',
                message='Expiry date must be in format: MM/YY'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YY',
            'id': 'expiry_date'
        }),
        required=False
    )
    
    cvv = forms.CharField(
        max_length=4,
        validators=[
            RegexValidator(
                regex=r'^\d{3,4}$',
                message='CVV must be 3 or 4 digits'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CVV',
            'id': 'cvv'
        }),
        required=False
    )
    
    save_card = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'save_card'
        })
    )
    
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'terms_accepted'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method in ['credit_card', 'debit_card']:
            # Validate card fields for card payments
            card_fields = ['card_number', 'card_holder_name', 'expiry_date', 'cvv']
            for field in card_fields:
                if not cleaned_data.get(field):
                    raise forms.ValidationError(f"{field.replace('_', ' ').title()} is required for card payments.")
        
        return cleaned_data

class CouponForm(forms.Form):
    coupon_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter coupon code',
            'id': 'coupon_code'
        })
    )
    
    def clean_coupon_code(self):
        code = self.cleaned_data['coupon_code'].upper()
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.valid_until < timezone.now():
                raise forms.ValidationError('This coupon has expired.')
            return code
        except Coupon.DoesNotExist:
            raise forms.ValidationError('Invalid coupon code.')
