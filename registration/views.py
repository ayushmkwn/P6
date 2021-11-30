from django.shortcuts import render
from .forms import *
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, message
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .models import users
from django.db.models import Q
from datetime import date
from Practical_6 import settings
from .tokens import generate_token
# Create your views here.
x = 0


def home(request):
    return render(request, 'home.html')


def valid_data(form):
    q1 = users.objects.filter(Q(email=form.cleaned_data['email']) | Q(
        mobileno=form.cleaned_data['mobileno']))
    if q1:
        return False, 'Account already exist!'

    if form.cleaned_data['password'] != form.cleaned_data['confirmpassword']:
        return False, 'Passwords do not match!'

    birthdate = form.cleaned_data['birthdate']
    today = date.today()
    age = today.year - birthdate.year - \
        ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 18:
        return False, 'Your age is less than 18 years!'

    try:
        q = users.objects.get(username=form.cleaned_data['username'])
        return False, 'Username already exist!'
    except:
        pass

    form.save()
    return True, 'Successfully Registered!'


def register(request):
    global x
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                okay, message = valid_data(form)
                new_user = users.objects.get(email=form.cleaned_data['email'])
                current_site = get_current_site(request)
                email_subject = "Confirm your email @Social Media Login!"
                email_message = render_to_string('email_confirmation.html', {
                    'name': new_user.name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': generate_token.make_token(new_user)})
                email_send = EmailMessage(
                    email_subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [new_user.email])
                email_send.fail_silently = True
                email_send.send()

                if okay:
                    x = 1
                    messages.success(
                        request, 'Activate your account from email!')
                    return redirect("/")
                else:
                    return render(request, 'register.html', {'message': message, 'form': form})
            else:
                return render(request, 'register.html', {'message': "Something wrong!", 'form': form})

        except Exception as e:
            print(e)
            return render(request, 'register.html', {'message': message, 'form': form})

    form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        new_user = users.objects.get(email=uid)
    except Exception as e:
        print(e)
        new_user = None

    if new_user is not None and generate_token.check_token(new_user, token):
        new_user.is_authenticatedd = True
        # user.profile.signup_confirmation = True
        new_user.save()
        # login(request,new_user)
        # signin(request)
        messages.success(request, 'Your account successfully activated!')
        return redirect("/signin/")
    else:
        return render(request, 'error.html')


def signin(request):
    global x

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                c_user = users.objects.filter(Q(email=form.cleaned_data['email']) | Q(
                    mobileno=form.cleaned_data['email']))
                c_user = c_user.get(password=form.cleaned_data['password'])
                if c_user.is_authenticatedd:
                    request.session['cr_user'] = c_user.name
                    request.session['cr_email'] = c_user.email
                    return render(request, 'home.html', {'obj': c_user})
                else:
                    return render(request, 'signin.html', {'form': form, 'message': 'Authentication Required!'})
            except Exception as e:
                print(e)
                return render(request, 'signin.html', {'form': form, 'message': 'Password dose not match!'})
        else:
            return render(request, 'signin.html', {'form': form, 'message': 'Not allowed!'})

    else:
        form = LoginForm()

    message = ''
    if x == 1:
        message = 'Account Created Successfully!'
        x = 0

    return render(request, 'signin.html', {'form': form, 'message': message})


def signout(request):
    logout(request)
    return redirect("/")
