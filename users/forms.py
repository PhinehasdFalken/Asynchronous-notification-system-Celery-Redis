from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from users.models import NewUser

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address")

    class Meta:
        model = NewUser
        # all items in the turple except email are fields defined in the UserCreationForm model according to fields defined in your custom user model
        fields = ('email', 'user_name', 'first_name', 'password1', 'password2')


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = NewUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")
    

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        try:
            account = NewUser.objects.get(user_name=user_name)
        except Exception as e:
            return user_name
        raise forms.ValidationError(f"Username {user_name} is already in use.")


# Login form
class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')
