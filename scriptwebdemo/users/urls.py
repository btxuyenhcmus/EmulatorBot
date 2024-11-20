from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('user', views.user, name='user'),
    path('', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('multilogin/', views.multilogin, name='multilogin'),
    path('create-script/', views.create_script, name='create_script'),
    path('multilogin/run/<int:scriptId>', views.run_script,
         name='run_script'),
    path('fetch-scripts/', views.fetch_scripts, name='fetch_scripts'),
    path('delete-script/<int:scriptId>',
         views.delete_script, name='delete_script')
]
