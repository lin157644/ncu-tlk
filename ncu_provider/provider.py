from urllib.parse import parse_qsl
from django.urls import reverse
from django.utils.http import urlencode

from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import AuthAction, ProviderAccount
from allauth.socialaccount.providers.base import Provider
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

class Scope(object):
    ID = "id"
    IDENTIFIER = "identifier"
    CH_NAME = "chinese-name"
    EMAIL = "email"

class NCUAccount(ProviderAccount):
    def to_str(self):
        dflt = super(NCUAccount, self).to_str()
        return self.account.extra_data.get("name", dflt)

class NCUProvider(OAuth2Provider):
    id = "ncu"
    name = "ncu"
    account_class = NCUAccount

    def get_default_scope(self):
        return [Scope.ID, Scope.IDENTIFIER, Scope.CH_NAME, Scope.EMAIL]

    "The provider must implement the `extract_uid()` method"
    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        return dict(
            email=data.get("email"),
        )

    def extract_email_addresses(self, data):
        ret = []
        print(data.get("email"))
        ret.append(EmailAddress(email=data.get("email"), verified=True, primary=True))
        return ret


provider_classes = [NCUProvider]