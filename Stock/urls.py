from django.urls import path, re_path 
from . import views

urlpatterns = [                             
    path("", view=views.home, name="index"),
    path('get_chart/', views.get_chart, name='get_chart'),
    path("renew/", views.get , name="getdata"),
    path("GS/", views.search , name="search"),
    re_path("GS/$", views.search , name="search"),

]
