from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ChoiceField, CharField
from django.forms.fields import BooleanField
from django.forms.widgets import CheckboxInput, PasswordInput

from django.utils.translation import ugettext as _


class SecurityForm(ModelForm):
    new_password = CharField(widget=PasswordInput, required=False)
    repeat_new_password = CharField(widget=PasswordInput, required=False)
    change_password = BooleanField(required=False)
    current_password = CharField(widget=PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SecurityForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password', '')
        if not self.request.user.check_password(current_password):
            raise ValidationError(_('The current password is incorrect.'))
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if self.cleaned_data['change_password'] and not new_password:
            raise ValidationError(_('The password can not be empty.'))
        return new_password

    def clean_repeat_new_password(self):
        new_password = self.cleaned_data.get('new_password', '')
        repeat_new_password = self.cleaned_data.get('repeat_new_password', '')
        if self.cleaned_data['change_password'] and new_password != repeat_new_password:
            raise ValidationError(_('Password do not match.'))
        return repeat_new_password




    class Meta:
        fields = ('email', 'change_password', 'new_password', 'repeat_new_password')
        model = get_user_model()
