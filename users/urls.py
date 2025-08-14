from django.urls import path
from .views import register_view
from . import views
from django.contrib.auth.views import LoginView, LogoutView

# URL для входа
urlpatterns = [
    # path('', views.index, name='index'),
    path('register/', register_view, name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', views.UserListView.as_view(), name='users'),
]