from django import forms 
from django.contrib.auth.forms import (UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm
                                            ,SetPasswordForm)
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Event,Feedback
from django.urls import reverse_lazy
from .models import Organizer
# using form-control we use Bootstrap 

class UserRegistrationForm(UserCreationForm):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email=forms.CharField(required=True,label='Email',widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class': 'form-control'}))
    password=forms.CharField(required=True,label=_("Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control' }))

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password','class': 'form-control' }))
    new_password1 = forms.CharField(label=_("New Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password','class': 'form-control' }),
    help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=_("Confirm New Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password','class': 'form-control' }),
    )

class MypasswordResetForm(PasswordResetForm):
    # don't need to remember below field you can see it by commmand and paste when you need  it
    email=forms.EmailField(label=_('Email'), max_length=254,widget=forms.EmailInput(attrs={'autocomplete':"email", 'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password','class': 'form-control' }),
    help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=_("Confirm New Password"),strip=False,
    widget=forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password','class': 'form-control' }))



class OrganizerRegistrationForm(forms.ModelForm):
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    organization_name = forms.CharField(label=_('Organization Name'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_email = forms.EmailField(label=_('Contact Email'), widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contact_phone = forms.CharField(label=_('Contact Phone Number'), required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    organization_address = forms.CharField(label=_('Organization Address'), required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_organizer = forms.BooleanField(label=_("Is Organizer"), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'organization_name', 'contact_email', 'contact_phone', 'organization_address']


class OrganizerLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(
        required=True,
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'})
    )


    def get_success_url(self):
        if self.cleaned_data['is_organizer']:
            return reverse_lazy('app:CreateEvent')
        return super().get_success_url()
    
class OrganizerChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'autocomplete': 'current-password', 'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'autocomplete': 'current-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'autocomplete': 'current-password', 'class': 'form-control'})
    )

class OrganizerPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': "email", 'class': 'form-control'})
    )

class OrganizerSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'autocomplete': 'current-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'autocomplete': 'current-password', 'class': 'form-control'})
    )


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'venue', 'date', 'time', 'description', 'organizer_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # Assuming organizer_image and organizer_upload are FileInput fields
            'organizer_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Rating (1-5)',
            'comment': 'Comment'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4})
        }