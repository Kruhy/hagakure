from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.views import View

from utils.functions import display_name

User = get_user_model()

from .forms import SignUpForm, UserRegistrationForm


class RegisterUser(View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_staff:
            raise Http404

        context = {
            'name': display_name(request.user),
            'password': User.objects.make_random_password(),
            }

        return render(request, 'registration/register_user.html', context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            mail_subject = 'Jednorazowy link do rejestracji na stronie hagakure.pl'
            html_message = render_to_string('registration/confirmation_email.html', context)
            plain_message = strip_tags(html_message)
            to_email = form.cleaned_data.get('email')
            email = EmailMultiAlternatives(
                mail_subject,
                plain_message,
                from_email='hagakure.pl <kontakt@hagakure.pl>',
                to=[to_email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            messages.success(
                request,
                'Wiadomość email wysłana na adres {}. Użytkownik będzie mógł dokończyć rejestrację po kliknięciu w wysłany link'.format(user.email)
                )
        
        return redirect('add_user')


class ActivateUser(View):
    
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request,
                'Miło, że z nami jesteś! Uzupełnij profil, aby dokończyć rejestrację!'
                )

            context = {
                'name': display_name(request.user),
                'email': user.email,
                }

            return render(request, 'registration/registration_form.html', context)

        else:
            return HttpResponse('Activation link is invalid!')
        
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if form.data['password'] != form.data['password2']:
                messages.error(
                    request,
                    'Podane hasła są rózne! Spróbuj jeszcze raz!'
                    )
                context = {
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'nick': data['nick'],
                    'phone_number': data['phone_number'],
                    'ice_contact_name': data['ice_contact_name'],
                    'ice_contact_number': data['ice_contact_number'],
                    'birth_date': data['birth_date'],
                    }
                return render(request, 'registration/registration_form.html', context)

            user = User.objects.filter(email=form.data['email']).get()

            user.set_password(data['password'])
            user.first_name = data['first_name']
            user.last_name = data['last_name']

            if data['nick'] != '':
                user.nick = data['nick']

            user.phone_number = data['phone_number']
            user.ice_contact_name = data['ice_contact_name']
            user.ice_contact_number = data['ice_contact_number']

            if data['birth_date'] != '':
                user.birth_date = data['birth_date']
            
            user.save()

            login(request, user)

            return redirect('user_details')

        messages.error(request, 'Błąd, spróbuj ponownie')

        context = {
            'email': form.data['email'],
            'first_name': form.data['first_name'],
            'last_name': form.data['last_name'],
            'nick': form.data['nick'],
            'phone_number': form.data['phone_number'],
            'ice_contact_name': form.data['ice_contact_name'],
            'ice_contact_number': form.data['ice_contact_number'],
            'birth_date': form.data['birth_date'],
            }
        return render(request, 'registration/registration_form.html', context)
