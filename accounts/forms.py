from django import forms
from .models import *
from	django.utils.translation	import	gettext_lazy	as	_



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password confirmation',widget=forms.PasswordInput())

    class Meta:
        model = customUser
        fields	=	('username','email','phone',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

        


class searchForm(forms.Form):
    search = forms.CharField()


class filterForm(forms.Form):
    NEGOTIATION = (
        ('accept',_('Accept')),
        ('refuse',_('Refuse')),
        )
    PHONE_STATUS = (
    ('4/10','4/10'),('5/10','5/10'),('6/10','6/10'),
    ('7/10','7/10'),('8/10','8/10'),('9/10','9/10'),
    ('10/10','10/10'),
        )
    OFFER = (
        ('selling',_('Selling')),
        ('Buying',_('Buying')),
            )

    name = forms.CharField(widget = forms.TextInput(attrs={'placeholder':_('Name')}),localize=True )
    exchange = forms.ChoiceField(choices = NEGOTIATION )
    min_price = forms.DecimalField(max_digits=15,decimal_places=5 ,widget = forms.TextInput(attrs={'placeholder':_('Min Price in Da')}),localize=True )
    max_price = forms.DecimalField( max_digits=15,decimal_places=5 ,widget = forms.TextInput(attrs={'placeholder':_('Max Price in Da')}),localize=True )
    wilaya =forms.CharField(widget = forms.TextInput(attrs={'placeholder':_('Wilaya')}),localize=True )
    phoneStatus = forms.ChoiceField(choices = PHONE_STATUS)
    offer = forms.ChoiceField(choices = OFFER )
    description = forms.CharField(widget = forms.TextInput(attrs={'placeholder':_('Description')}),localize=True )


class emailForm(forms.ModelForm):
    subject = forms.CharField(max_length = 40)
    my_email = forms.EmailField()
    my_message = forms.TextInput()
