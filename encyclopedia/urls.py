from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.navigate, name="navigate"),
    path("newpage/", views.new_page, name="newpage"),
    path("random/", views.random, name="random")
]
