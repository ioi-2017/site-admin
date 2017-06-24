from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile


class LoginRequiredMiddleware(object):
    def process_request(self, request):
        print(request.path_info)
        # if not request.user.is_authenticated():
        #     print(request.path_info)
        #     path = request.path_info.lstrip('/')
        #     if not any(m.match(path) for m in EXEMPT_URLS):
        #         return HttpResponseRedirect(settings.LOGIN_URL)
