from django.urls import path

from appbase.views.token_pair import TokenPairView
from appbase.views.refresh_token import CustomRefreshTokenView


urls = (
   path('token', TokenPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh', CustomRefreshTokenView.as_view(), name='token_refresh'),
)