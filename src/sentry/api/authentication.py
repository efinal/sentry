from sentry.models import ProjectKey

from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed


class KeyAuthentication(BasicAuthentication):
    def authenticate_credentials(self, userid, password):
        try:
            pk = ProjectKey.objects.get_from_cache(public_key=userid)
        except ProjectKey.DoesNotExist:
            raise AuthenticationFailed('Invalid api key')

        if pk.secret_key != password:
            raise AuthenticationFailed('Invalid api key')

        return (pk.user, pk)
