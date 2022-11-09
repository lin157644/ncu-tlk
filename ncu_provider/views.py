import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import NCUProvider


class NCUOAuth2Adapter(OAuth2Adapter):
    provider_id = NCUProvider.id
    access_token_url = "https://portal.ncu.edu.tw/oauth2/token"
    authorize_url = "https://portal.ncu.edu.tw/oauth2/authorization"
    profile_url = "https://portal.ncu.edu.tw/apis/oauth/v1/info"

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer '+token.token}
        resp = requests.get(
            self.profile_url,
            headers=headers,
        )
        resp.raise_for_status()
        extra_data = resp.json()
        print("Data:", extra_data)
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login


oauth2_login = OAuth2LoginView.adapter_view(NCUOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(NCUOAuth2Adapter)
