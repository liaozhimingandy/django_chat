from django.urls import path

from oauth.views import AuthorizeView, TokenRefreshView, TestOauthView

# url 命令空间
app_name = 'oauth'

urlpatterns = [
    path("authorize/<uuid:app_id>/<str:app_secret>/<str:grant_type>/", AuthorizeView.as_view(), name='authorize'),
    path("refresh-token/<uuid:app_id>/<str:grant_type>/", TokenRefreshView.as_view(), name='refresh_token'),
    path("test-oauth/", TestOauthView.as_view(), name='test_oauth')
]