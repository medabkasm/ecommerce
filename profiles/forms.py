from django import forms
from accounts.models import *
from	django.utils.translation	import	gettext_lazy	as	_


class profileEditForm(forms.ModelForm):     # form for creating / editing  a profile
    class Meta:
        model = Profile
        fields = ('first_name','last_name','type','image','address','country','state',)
        widgets = {
            'image':forms.FileInput,
        }

class userEditForm(forms.ModelForm):
    class Meta:
        model = customUser
        fields = ('username','phone','email')


class postForm(forms.Form):   # for for share new post

    OFFER = (
        ('selling',_('Selling')),
        ('Buying',_('Buying')),
            )

    STATUS = (
			('hide',_('Hide')),
			('publish',	_('Publish')),
				)

    NEGOTIATION = (
        ('accept',_('Accept')),
        ('refuse',_('Refuse')),
        )
    PHONE_STATUS = (
    ('4/10','4/10'),('5/10','5/10'),('6/10','6/10'),
    ('7/10','7/10'),('8/10','8/10'),('9/10','9/10'),
    ('10/10','10/10'),
    )

    name = forms.CharField()
    offer = forms.ChoiceField(choices = OFFER )
    phone = forms.CharField()
    status	= forms.ChoiceField(choices=STATUS)
    exchange = forms.ChoiceField(choices = NEGOTIATION )
    negotiation = forms.ChoiceField(choices = NEGOTIATION)
    price = forms.DecimalField( max_digits=15,decimal_places=5)
    wilaya =forms.CharField()
    description = forms.CharField(widget = forms.TextInput())
    coverImg = forms.ImageField(widget = forms.FileInput)
    phoneStatus = forms.ChoiceField(choices = PHONE_STATUS)


class postEditForm(forms.ModelForm):
    class Meta:
        model = userPosts
        fields = ('name','offer','phone','status','exchange','negotiation','price','wilaya','description','coverImg','phoneStatus',)
        widgets = {
            'coverImg':forms.FileInput,
        }

class imageEditForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
        widgets = {
            'image':forms.FileInput,
        }
