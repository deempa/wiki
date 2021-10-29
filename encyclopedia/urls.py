from django.urls import path
from django.urls.conf import include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryname>", views.entry, name="entry"),
    path("wiki/", views.search, name="search"),
    path("wiki/newpage/", views.newpage, name="newpage"),
    path("wiki/editpage/<str:entryname>", views.editpage, name="editpage"),
    path("randompage", views.randompage, name='randompage')
]
