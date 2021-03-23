import json

import requests as recaptcha_request
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse

from the_elder_commands.utils.messages_system import MessagesSystem


def check_recaptcha(site):
    def decorator(func):
        def wrapper(request):
            recaptcha_data = {"response": request.POST.get("g-recaptcha-response"),
                              "secret": settings.RECAPTCHA_SECRET_KEY}
            recaptcha_response = recaptcha_request.post("https://www.google.com/recaptcha/api/siteverify",
                                                        recaptcha_data)
            result = json.loads(recaptcha_response.content)
            if result.get("success") and result.get("score") >= 0.4:
                func(request)
            else:
                messages = MessagesSystem(request)
                url = HttpRequest.build_absolute_uri(request, reverse('main_page:about_me'))
                getattr(messages, "append_" + site)("It looks like you're a bot. If not, contact me the other way. "
                                                    f"{url}")
        return wrapper
    return decorator