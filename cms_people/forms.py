from django.contrib.auth import get_user_model
from django.forms import ModelForm, ChoiceField, CharField
from django.forms.fields import BooleanField
from django.forms.widgets import CheckboxInput, PasswordInput


class SecurityForm(ModelForm):
    new_password = CharField(widget=PasswordInput)
    repeat_new_password = CharField(widget=PasswordInput)
    change_password = BooleanField()
    current_password = BooleanField(widget=PasswordInput)


    class Meta:
        fields = ('email', 'change_password', 'new_password', 'repeat_new_password')
        model = get_user_model()
