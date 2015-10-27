# coding=utf-8
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core import validators
from django.utils.translation import ugettext_lazy as ugettext
from bubble.forms import BootstrapFormMixin
from users.models import User, UserWallPost


class ProfileSettingsForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'gender', 'birth_date', 'city', 'job', 'about_me', 'interests')

    def __init__(self, *args, **kwargs):
        super(ProfileSettingsForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)
        self.fields['birth_date'].widget.attrs['placeholder'] = ugettext(u'Введіть дату у форматі РРРР-ММ-ДД')
        self.fields['about_me'].widget.attrs['rows'] = 3
        self.fields['interests'].widget.attrs['rows'] = 3


class UserChangePasswordForm(PasswordChangeForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)
        for field_name in ('old_password', 'new_password1', 'new_password2'):
            self.fields[field_name] = self.fields.pop(field_name)
            if field_name != 'old_password':
                self.fields[field_name].validators.extend([validators.MinLengthValidator(4),
                                                           validators.MaxLengthValidator(40)])


class UserChangeEmailForm(forms.Form, BootstrapFormMixin):
    new_email = forms.EmailField(max_length=75, label=ugettext(u'новий email'))
    password = forms.CharField(label=(ugettext(u'поточний пароль')), min_length=6, max_length=40,
                               widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserChangeEmailForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email'].strip()
        if User.objects.filter(email=new_email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError(ugettext(u'Користувач з таким email вже зареєстрований'))
        return new_email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError(ugettext(u'Невірно введений пароль'))
        return password

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email']
        if commit:
            self.user.save()
        return self.user


class WallPostForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = UserWallPost
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': ugettext(u'напишіть на стіні...'), 'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super(WallPostForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def clean_content(self):
        return self.cleaned_data['content'].strip()


class SearchPeopleForm(forms.Form, BootstrapFormMixin):
    fname_and_lname = forms.CharField(label=ugettext(u"ім'я, прізвище"), required=False)
    gender = forms.TypedChoiceField(label=ugettext(u'стать'),
                                    choices=((0, ugettext(u'всі')),) + User.GENDER_CHOICES[1:],
                                    coerce=lambda val: int(val), required=False)
    from_date = forms.IntegerField(label=ugettext(u'рік народження з'), required=False,
                                   widget=forms.NumberInput(attrs={'placeholder': ugettext(u'від')}))
    to_date = forms.IntegerField(label=ugettext(u'рік народження до'), required=False,
                                 widget=forms.NumberInput(attrs={'placeholder': ugettext(u'до')}))
    city = forms.CharField(label=ugettext(u'місто'), required=False)
    job = forms.CharField(label=ugettext(u'робота'), required=False)
    about_me = forms.CharField(label=ugettext(u'про себе'), required=False)
    interests = forms.CharField(label=ugettext(u'інтереси'), required=False)

    def __init__(self, *args, **kwargs):
        super(SearchPeopleForm, self).__init__(*args, **kwargs)
        BootstrapFormMixin.__init__(self)

    def get_values_list(self, field_name):
        val = self.cleaned_data.get(field_name)
        if isinstance(val, basestring):
            val = val.strip().split()
        return val or []
