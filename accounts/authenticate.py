from .models import	customUser


class	emailAuthBackend(object):
    """
    Authenticate	using	an	e-mail	address.
    """
    def	authenticate(self,	request,	username=None,	password=None):
        try:
            user = User.objects.get(email = username )
            if	user.check_password(password):
                return	user
            return	None
        except	User.DoesNotExist:
            return	None

    def	get_user(self,	user_id):
        try:
            return	User.objects.get(pk=user_id)
        except	customUser.DoesNotExist:
            return	None


class phoneAuthBackend(object):
    """
    Authenticate	using	a phone number.
    """
    def	authenticate(self,	request,	username=None,	password=None):
        try:
            user = User.objects.get(phone = username )
            if	user.check_password(password):
                return	user
            return	None
        except	User.DoesNotExist:
            return	None

    def	get_user(self,	user_id):
        try:
            return	mUser.objects.get(pk=user_id)
        except	User.DoesNotExist:
            return	None
