from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView

from pkg_helpers.exceptions.auth import UnVerifiedException
from pkg_helpers.response.response import RestResponse
from appbase.services.user import UserService

class TokenPairView(TokenObtainPairView):
    _user_service = UserService()

    def post(self, request: Request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        
            return RestResponse().success().set_data(
                {
                    **response.data,
                    "user": self._user_service.get_user_by_email(request.data["email"])
                }
            ).response
        except serializers.ValidationError:
            return RestResponse().validation_failed().set_message("Dữ liệu đầu vào không hợp lệ!").response
        except UnVerifiedException as e:
            _email = request.data["email"]
            # TODO
            # self.account_service.resend_registration_otp(_email)
            return RestResponse().direct(f"/otp/{_email}").response
        except exceptions.AuthenticationFailed as e:
            return RestResponse().defined_error().set_message("Thông tin tài khoản không chính xác!").response
        except exceptions.PermissionDenied as e:
            return RestResponse().defined_error().set_message("Tài khoản đã bị khóa!").response