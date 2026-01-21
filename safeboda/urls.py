# filepath: /Users/Lenovo/caching-gla-go-getter/safeboda/urls.py
from django.contrib import admin
from django.urls import path, include

from .views import home  # import the home view

urlpatterns = [
    path("", home, name="home"),                 # root URL
    path("admin/", admin.site.urls),            # admin
    path("api/users/", include("users.urls")),  # users API
]