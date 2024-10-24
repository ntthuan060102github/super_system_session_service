import json
from enum import Enum
from typing import Union, Any
from django.core.cache import cache

from appbase.models.user import User

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.settings import api_settings as jwt_configs

from pkg_helpers.logging import logger
from pkg_helpers.auth.user_dto import UserDTO

class TokenTypes(Enum):
    access = "access"
    refresh = "refresh"

class SessionService():
    __base_access_token_class = AccessToken
    __base_refresh_token_class = RefreshToken
    __prefix_key = "session"

    def verify_token(self, token: str) -> bool:
        try:
            user_id = self.__base_access_token_class(token=token).payload.get("user_id", None)
            jti = self.__base_access_token_class(token=token).payload["jti"]
            return cache.has_key(f"{self.__prefix_key}:{user_id}:{TokenTypes.access.value}:{jti}")
        except Exception as e:
            logger.exception("SessionService.verify_token exc=%s", e)
            return False
        
    def verify_refresh_token(self, token: str) -> bool:
        try:
            user_id = self.__base_refresh_token_class(token=token).payload.get("user_id", None)
            jti = self.__base_refresh_token_class(token=token).payload["jti"]
            return cache.has_key(f"{self.__prefix_key}:{user_id}:{TokenTypes.refresh.value}:{jti}")
        except Exception as e:
            logger.exception("SessionService.verify_refresh_token exc=%s", e)
            return False

    def get_context(self, token: str) -> Union[UserDTO, None]:
        try:
            token_payload = self.__base_access_token_class(token=token).payload
            user_id = token_payload.get("user_id", None)
            jti = token_payload.get("jti", None)
            session_data = json.loads(cache.get(f"{self.__prefix_key}:{user_id}:{TokenTypes.access.value}:{jti}"))
            return UserDTO(**session_data)
        except Exception as e:
            logger.exception("SessionService.get_context exc=%s", e)
            return None
        
    def __save_token_pair(self, key: Any, data: Any, access_jti: str, refresh_jti: str):
        self.__remove_token(key, TokenTypes.access)
        self.__remove_token(key, TokenTypes.refresh)
        cache.set(f"{self.__prefix_key}:{str(key)}:{TokenTypes.access.value}:{access_jti}", json.dumps(data), jwt_configs.ACCESS_TOKEN_LIFETIME.seconds)
        cache.set(f"{self.__prefix_key}:{str(key)}:{TokenTypes.refresh.value}:{refresh_jti}", json.dumps(data), jwt_configs.ACCESS_TOKEN_LIFETIME.seconds)

    def __remove_token(self, key: Any, type: TokenTypes):
        cache.delete_many(cache.keys(f"{self.__prefix_key}:{str(key)}:{type.value}:*"))

    def save_session(self, user: User, access_jti: str, refresh_jti: str):
        self.__save_token_pair(user.id, user.to_dto(), access_jti, refresh_jti)

    def remove_session(self, user_id: int):
        self.__remove_token(user_id, TokenTypes.access)
        self.__remove_token(user_id, TokenTypes.refresh)