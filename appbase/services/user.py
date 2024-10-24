from pkg_helpers.logging import logger
from typing import Union, Any

from appbase.repositories.user import UserRepo

from pkg_helpers.auth.user_dto import UserDTO

class UserService():
    _user_repo = UserRepo()

    def get_user_by_email(self, email: str) -> Union[UserDTO, None]:
        try:
            user = self._user_repo.get_user_by_email(email=email)
            
            if user is None:
                return None

            return user.to_dto()
        except Exception as e:
            logger.exception("UserService.get_user_by_email exc=%s, email=%s", e, email)
            raise e
        
    def get_user_by_id(self, id: Any) -> Union[UserDTO, None]:
        try:
            user = self._user_repo.get_user_by_id(id=id)
            
            if user is None:
                return None

            return user.to_dto()
        except Exception as e:
            logger.exception("UserService.get_user_by_id exc=%s, id=%s", e, id)
            raise e