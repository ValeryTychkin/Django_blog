from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserPageForm(forms.Form):
    """
        Форма для правки информации о пользователе в /app_users/full_size/user_page.html
    """
    f_name = forms.CharField(max_length=150,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                             }))
    l_name = forms.CharField(max_length=150,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                             }))
    about = forms.CharField(required=False, max_length=500,
                            widget=forms.Textarea(attrs={
                                'class': 'form-control',
                                'id': 'aboutTextarea',
                                'placeholder': 'label',
                                'style': 'height: 100px',
                            }))
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(attrs={
                                  'class': 'user-upload-avatar-file',
                                  'accept': 'image/jpeg',
                                  'id': 'id_avatar',
                                  'onchange': 'previewImage();',
                              }))


class LoginForm(forms.Form):
    """
        Форма для входа пользователя на всех страницах, где используется /main_base.html
    """
    username = forms.CharField(min_length=2, max_length=35,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control form-control-sm',
                                   'placeholder': 'Логин',
                               }))
    password = forms.CharField(min_length=3, max_length=30,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control form-control-sm',
                                   'placeholder': 'Пароль',
                               }))


class RegisterForm(UserCreationForm):
    """
        Форма для регистрации пользователя в /app_users/full_size/sign_up.html
    """
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(attrs={
                                  'class': 'user-upload-avatar-file',
                                  'accept': 'image/jpeg',
                                  'onchange': 'previewImage();',
                              }))
    about = forms.CharField(required=False, max_length=500,
                            widget=forms.Textarea(attrs={
                                'class': 'form-control',
                                'id': 'aboutTextarea',
                                'placeholder': 'label',
                                'style': 'height: 100px',
                            }))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs = {
            'class': 'form-control mb-2',
            'placeholder': 'Пароль',
        }

        self.fields['password2'].widget.attrs = {
            'class': 'form-control mb-3',
            'placeholder': 'Повторить Пароль',
        }

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'avatar', 'about')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Логин',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Имя',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Фамилия',
            }),
        }
