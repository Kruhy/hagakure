from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

User = get_user_model()
from .forms import SignUpForm


class RegisterUser(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/register_user.html')

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Jednorazowy link do rejestracji na stronie hagakure.pl'
            message = render_to_string('registration/confiramtion_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(
                render,
                'Wiadomość email wysłana na adres {}. Użytkownik będzie mógł dokończyć rejestrację po kliknięciu w wysłany link'.format(user.email)
                )

            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = SignUpForm()
        return render(request, 'registration/register_user.html')


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
            messages.success(
                render,
                'Miło, że z nami jesteś! Uzupełnij profil, aby dokończyć rejestrację!'
                )
            #TODO: redirect to user profile edit, add msg
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')
