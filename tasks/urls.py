from django.urls import path
from django.conf.urls import url


from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:task_id>/', views.details, name='detail'),
    path('create/<category>/', views.create, name='create'),
    path('edit/<int:task_id>/',views.edit,name="edit"),
    path('delete/<int:task_id>/', views.delete, name='delete'),
    path('add_category/',views.add_category,name="add_category"),
    path('register/',views.register,name="register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]