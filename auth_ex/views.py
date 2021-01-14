from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.views import View

from .forms import ChageEmailForm, LogInForm, UserDetailsForm, VerifyPasswordForm


User = get_user_model()


class LogInView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'auth_ex/login.html')

    def post(self, request, *args, **kwargs):

        form = LogInForm(request.POST)

        #TODO: fix cleaned_data!

        # import pdb; pdb.set_trace()

        # if form.is_valid():
            
        #     data = form.cleaned_data

        data = form.data
        user = authenticate(request, email=data['email'], password=data['password'])

        if user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            messages.warning(request, 'Błędny adres email lub hasło!')
            return render(request, 'auth_ex/login.html')


class LogOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('landing_page')



class UserDetailsView(View):

    def get(self, request, *args, **kwargs):
        
        context = {
            'name': display_name(request.user),
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'nick': request.user.nick,
            'email': request.user.email,
            'phone': request.user.phone_number,
            'ice': request.user.ice_contact_name,
            'ice_phone': request.user.ice_contact_number,
            'birth_date': request.user.birth_date,
            'register_date': request.user.date_joined,
        }
        return render(request, 'auth_ex/user_details.html', context)



class UserDetailsEdit(View):

    def get(self, request, *args,**kwargs):
        context = {
            'name': display_name(request.user),
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'nick': request.user.nick,
            'phone': request.user.phone_number,
            'ice': request.user.ice_contact_name,
            'ice_phone': request.user.ice_contact_number,
            'birth_date': request.user.birth_date,
        }
        return render(request, 'auth_ex/user_edit.html', context)

    def post(self, request, *args, **kwargs):
        form = UserDetailsForm(request.POST)
        user = request.user

        if form.is_valid():
            data = form.cleaned_data
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.nick = data['nick']
            user.phone_number = data['phone_number']
            user.ice_contact_name = data['ice_contact_name']
            user.ice_contact_number = data['ice_contact_number']
            user.birth_date = data['birth_date']
            user.save()

            messages.success(request, 'Dane poprawnie zmienione')
            return redirect('user_details')
        
        messages.error(request, "Błąd! Spróbój ponownie!")
        return redirect('user_edit')



class VerifyPasswordView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'name': display_name(request.user),
        }
        return render(request, 'auth_ex/verify_password.html', context)
    
    def post(self, request, *args, **kwargs):
        form = VerifyPasswordForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data

            if check_password(data['password'], request.user.password):
                return redirect('change_email')
            
            messages.error(request, "Błędne hasło! Spróbuj ponownie!")
            return redirect('verify_password')



class ChangeEmailView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'name': display_name(request.user),
        }
        return render(request, 'auth_ex/change_email.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ChageEmailForm(request.POST)
        user = request.user

        if form.is_valid():
            data = form.cleaned_data
            
            if form.data['email'].lower() != form.data['email2'].lower():
                messages.error(request, 'Podane adresy email są różne! Spróbój ponownie!')
                return redirect('change_email')
            
            if User.objects.filter(email=data['email']).count() != 0:
                messages.error(request, 'Podane adresy email istnieje w naszej bazie! Wprowadź inny adres!')
                return redirect('change_email')

            user.email = data['email']
            user.save()

            messages.success(request, 'Adres email zmieniony poprawnie!')
            return redirect('user_details')

        messages.error(request, 'Wystąpił błąd! Spróbój ponownie!')
        return redirect('change_email')



class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'name': display_name(request.user),
        }
        return render(request, 'auth_ex/change_password.html', context)
    
    def post(self, request, *args, **kwargs):
        form = VerifyPasswordForm(request.POST)
        user = request.user

        if form.is_valid():
            data = form.cleaned_data

            if check_password(data['password'], request.user.password):

                if form.data['new_password1'] != form.data['new_password2']:
                    messages.error(request, 'Podane hasła są różne! Spróbój ponownie!')
                    return redirect('change_password')
            
                user.set_password(form.data['new_password1'])
                user.save()
                login(request, user)

                messages.success(request, 'Hasło poprawnie zmenione!')
                return redirect('user_details') 

        messages.error(request, 'Niepoprawne hasło! Spróbój ponownie!')
        return redirect('change_password') 



def display_name(active_user):
    if active_user.is_authenticated:
        if active_user.nick:
            display_name = active_user.nick
        else:
            display_name = active_user.first_name

        return display_name
    return None
