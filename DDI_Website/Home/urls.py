from django.urls import path
from . import views as home_views


urlpatterns = [
    path('' , home_views.home_page , name = 'index-home'),
    path('login/', home_views.login_page, name = 'login-home'),
    path('logout/', home_views.logout_page, name = 'logout-home'),
    path('register/', home_views.registration_page, name = 'registration-home')
]