from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm
from .models import Contact

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact form data to the database
            contact = form.save()
            
            # Send email
            subject = f"New Contact Form Submission: {form.cleaned_data['subject']}"
            message = f"""
            Name: {form.cleaned_data['name']}
            Email: {form.cleaned_data['email']}
            Subject: {form.cleaned_data['subject']}
            Message: {form.cleaned_data['message']}
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.CONTACT_RECEIVER_EMAIL]
            
            try:
                # Send email to admin (existing functionality)
                send_mail(subject, message, from_email, recipient_list)
                
                # Send confirmation email to user
                user_subject = "Thank you for contacting us - XYZ Company"
                user_message = f"""
                Dear {form.cleaned_data['name']},
                
                Thank you for contacting XYZ Company. We have received your query and will get back to you as soon as possible.
                
                Your message details:
                Subject: {form.cleaned_data['subject']}
                Message: {form.cleaned_data['message']}
                
                We appreciate your patience and will respond to your inquiry shortly.
                
                Best regards,
                XYZ Company Team
                """
                
                # Send confirmation email to user
                send_mail(
                    user_subject, 
                    user_message, 
                    from_email, 
                    [form.cleaned_data['email']]
                )
                
                messages.success(request, 'Thank you for contacting us. We will get back to you soon.')
                return redirect('contact')
            except Exception as e:
                # Log the specific error for debugging
                print(f"Email error: {e}")
                messages.error(request, f'Email error: {str(e)}')
                # Delete the contact entry if email fails
                contact.delete()
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})