from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin

def simple_middleware(get_response):
    # One-time configuration and initialization.
    WHITELISTED_URLS = [
        reverse("authentication:ssologout"),
        reverse("main:homepage"),
        reverse("authentication:not_assign"),
        reverse("authentication:change_password"),
    ]
    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        if(request.user.is_authenticated and request.path[1:min(6,len(request.path)-1)] != "admin" and not (request.path in WHITELISTED_URLS) and request.user.role.role =="not-assign"):
            return HttpResponseRedirect(reverse("authentication:not_assign"))
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware