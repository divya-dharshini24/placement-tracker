from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("applications/", views.application_list, name="application_list"),
    path("applications/add/", views.add_application, name="add_application"),
    path("applications/<int:pk>/edit/", views.edit_application, name="edit_application"),
    path("applications/<int:pk>/delete/", views.delete_application, name="delete_application"),
]
