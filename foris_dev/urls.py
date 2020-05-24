"""foris_dev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from main_page import urls as main_page_urls
from lists import urls as lists_urls
from accounts import urls as accounts_urls
from rest_api.api_urls import router
from rest_api import api_urls
from the_elder_commands import urls as tec_urls

urlpatterns = [
    path("", include(main_page_urls)),
    path("lists/", include(lists_urls)),
    path("accounts/", include(accounts_urls)),
    path("api/", include(router.urls)),
    path("api/", include(api_urls)),
    path("the_elder_commands/", include(tec_urls)),
]
