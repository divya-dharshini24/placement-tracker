from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # login, logout and password views come from Django's built-in auth app
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("applications.urls")),
]
