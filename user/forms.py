from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.db import IntegrityError
from .models import Profile, User, HandProductSuplier


Gender_Choices = [('M', 'Male'), ('F', 'Female')]


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput)


    # username.widget.attrs.update({'id': 'username', 'width': '50px'})


class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(label="شماره تلفن", required=True)

    class Meta:
        model = User
        fields = ['email',
                  'password1', 'password2', 'phone']
        labels = {
            "email": "ایمیل",
            "password1": "رمز عبور",
            "password2": "تکرار رمز عبور",

        }

        help_texts = {
            "email": "ایمیل خود را به درستی وارد کنید",
        }

    def save(self, commit=True):
        '''
        override user create form to create profile after register!
        '''
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        try:
            # if commit:
            user.save()
            Profile.objects.create(user=user, phone=self.cleaned_data["phone"])

        except Exception as e:
            user.delete()
            raise ValueError(f"cant create profile object! reason: {e}")

        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['image']



class SuplierCreateForm(forms.ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=255,widget=forms.PasswordInput)
    phone= forms.CharField(max_length=20)
    
    class Meta:
        model = HandProductSuplier
        exclude = ["user",]


    def save(self, *args, **kwargs):
        try:
            email = self.cleaned_data["email"]
            password1 = self.cleaned_data["password1"]
            password2 = self.cleaned_data["password2"]
            if password1 == password2:
                user = User.objects.create_user(email=email, password=password1, phone=self.cleaned_data["phone"], is_staff=True)
                self.instance.user = user
                return super().save(*args, **kwargs)
            else:
                # TODO exception form
                raise Exception("pass1 va pass2 baiad barabar bashe")
        except:
            raise IntegrityError()


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="پسورد قدیمی",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )