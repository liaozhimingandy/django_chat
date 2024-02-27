from django.urls import path

from oauth.views import authorize, refresh_token, test_oauth

# url 命令空间
app_name = 'oauth'

urlpatterns = [
    path("authorize/<uuid:app_id>/<str:app_secret>/<str:grant_type>/", authorize, name='authorize'),
    path("refresh-token/<uuid:app_id>/<str:grant_type>/", refresh_token, name='refresh_token'),
    path("test_oauth/", test_oauth, name='test_oauth')
]