from typing import Union, Any

from appbase.models.user import User

class UserRepo():
    def get_user_by_email(self, email: str) -> Union[User, None]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
    def get_user_by_id(self, id: Any) -> Union[User, None]:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None