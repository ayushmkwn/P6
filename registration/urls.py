from django.urls.resolvers import URLPattern


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin/', views.signin, name="signin"),
    path('signout/',views.signout, name="signout")
]