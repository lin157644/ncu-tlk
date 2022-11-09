from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import NCUProvider


urlpatterns = default_urlpatterns(NCUProvider)
