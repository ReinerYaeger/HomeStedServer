"""
URL configuration for HomeStedConfig project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.homested, name='homested')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='homested')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include

from homested import views
#from subdomains.middleware import SubdomainURLRoutingMiddleware

urlpatterns = [
    path(os.getenv('ADMIN'), admin.site.urls),
    path('', include('homested.urls'))

]
# SUBDOMAIN_URLCONFS = {
#     None: 'HomeServer.urls',  # no subdomain, e.g. ``example.com``
#     'apartment': 'homested.urls',
# }

handler404 = views.response_error_handler
handler500 = views.response_error_handler
handler403 = views.response_error_handler
