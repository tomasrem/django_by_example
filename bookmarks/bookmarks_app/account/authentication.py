from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from account.models import Profile

# custom django authentication backend 
class EmailAuthBackend(BaseBackend):
    """
    Authenticate user using email adress.

    """
    def authenticate(self , request , username = None , password = None , **kwargs):
        try:
            user = User.objects.get(email = username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist , User.MultipleObjectsReturned):
            return None

    
    def get_user(self , user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    # custom auth backed has to have only those two class methods and work as above.

def create_profile(backend , user , *args , **kwargs):

    """
    Create user profile for social authentication
    
    """
    Profile.objects.get_or_create(user=user)