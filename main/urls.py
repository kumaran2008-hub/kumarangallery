from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("gallery/<slug:slug>/", views.category_detail, name="category_detail"),
    path("friends/", views.friends_list, name="friends_list"),
    path("friends/<slug:slug>/", views.friend_detail, name="friend_detail"),
]
