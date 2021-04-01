from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("my_view", views.my_view, name="my_view"),
]
