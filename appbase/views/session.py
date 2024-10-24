from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from appbase.validators.session import TokenValidator
from appbase.services.session import SessionService
from appbase.services.user import UserService

from pkg_helpers.auth.user_dto import UserDTO
from pkg_helpers.response.response import RestResponse
from pkg_helpers.logging import logger
from pkg_helpers.decorators.validate_request import validate_request

class SessionView(ViewSet):
    session_service = SessionService()
    user_service = UserService()

    @action(methods=["POST"], url_path="context", detail=False)
    @swagger_auto_schema(request_body=TokenValidator)
    @validate_request(TokenValidator)
    def get_session(self, request: Request) -> RestResponse:
        try:
            session_context = self.session_service.get_context(request.data["token"])

            if session_context is None:
                return RestResponse().invalid_token().response
            
            user = self.user_service.get_user_by_id(session_context.id)

            if user is None:
                return RestResponse().invalid_token().response
            
            return RestResponse().success().set_data(user).response
        except Exception as e:
            logger.exception("SessionView.get_session exc=%s, req=%s", e, request.data)
            return RestResponse().internal_server_error().response