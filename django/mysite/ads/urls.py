
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('create_ad', views.create_ad, name='create_ad'),
    path('ad/<int:ad_id>', views.ad, name='ad'),
    path('apply/<int:ad_id>', views.apply, name='apply'),
]