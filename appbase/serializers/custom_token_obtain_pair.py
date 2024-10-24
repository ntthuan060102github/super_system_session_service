from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from appbase.services.authentication import AuthenticationService

from pkg_helpers.enums.user_account_status import AccountStatuses
from pkg_helpers.exceptions.auth import UnVerifiedException
from pkg_helpers.logging import logger

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    authentication_service = AuthenticationService()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        try:
            validated_data = super().validate(attrs)
            refresh_jti = self.token_class(validated_data["refresh"]).payload["jti"]
            access_jti = self.token_class.access_token_class(validated_data["access"]).payload["jti"]
            self.authentication_service.save_session(self.user, access_jti, refresh_jti)

            return validated_data
        except AuthenticationFailed as e:
            if self.user is None:
                raise e
            
            elif self.user.status == AccountStatuses.BLOCKED:
                raise PermissionDenied("non activated account!")
            
            elif self.user.status == AccountStatuses.UNVERIFIED:
                raise UnVerifiedException("Unverified account!")
            
            raise e
        