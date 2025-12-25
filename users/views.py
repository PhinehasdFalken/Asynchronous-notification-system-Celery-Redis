from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .token import account_activation_token
from .models import NewUser
from users.forms import RegistrationForm, AccountAuthenticationForm
from notifications.tasks import send_activation_email_task, send_notification_task

# Create your views here.
def home_view(request):
    return render(request, 'users/home.html')

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Activate your account"
            # message = f"Hi {user.user_name}, click the activation link we sent to verify your account."
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            recipient = user.email

            send_activation_email_task.delay(recipient, subject, message)

            # email = form.cleaned_data.get('email').lower()
            # raw_password = form.cleaned_data.get('password1')
            # account = authenticate(email=email, password=raw_password)
            # login(request, account)
            # destination = get_redirect_if_exists(request)
            # if destination: # if destination != None
            #     return redirect(destination)
            # return redirect('home')
            return HttpResponse('Registered successfully and activation email sent! Check your email Inbox or Spam.')
        else:
            # returning the registration form back to the template if form is not valid(there are errors) 
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'users/register.html', context)


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = (NewUser.objects.get(pk=uid))
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        backend = 'django.contrib.auth.backends.AllowAllUsersModelBackend'
        login(request, user, backend=backend)
        send_notification_task.delay(
            user_id=user.id,
            event_type="user_signup",
            channel="email"
        )
        return redirect('home')
    else:
        return render(request, 'users/activation_invalid.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    context = {}

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user: # if user != None(if there is a user with the inputed email & password in the database)
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination: # if destination != None
                    return redirect(destination)
                return redirect('home')
        else:
            # returning the login form back to the template if form is not valid(there are errors) 
            context['login_form'] = form

    return render(request, 'users/login.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))
    return redirect
