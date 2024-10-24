from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenRefreshView

from pkg_helpers.response.response import RestResponse
from pkg_helpers.logging import logger

class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return RestResponse().success().set_data(response.data).response
        except Exception as e:
            logger.exception("CustomRefreshTokenView.post exc=%s", e)
            return RestResponse().direct("/login").set_message("Refresh token hết hạn hoặc không hợp lệ!").response