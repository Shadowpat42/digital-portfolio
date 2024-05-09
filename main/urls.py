from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/create", views.user_create, name="user_create"),
    path("event", views.event, name="event"),
    path("get_post/<int:post_id>", views.get_post, name="get_post"),
    path("methodological_resources", views.methodological_resources, name="methodological_resources"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path("user/<int:user_id>", views.user, name="user"),
    path('react_to_post/<int:post_id>/', views.react_to_post, name='react_to_post'),
    path("reward", views.reward, name="reward"),
]
