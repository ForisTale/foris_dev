from django.urls import path
from main_page import views


app_name = "main_page"

urlpatterns = [
    path("", views.home_page, name="home"),
    path("about_me", views.about_me, name="about_me"),
    path("contact", views.contact, name="contact"),
]
