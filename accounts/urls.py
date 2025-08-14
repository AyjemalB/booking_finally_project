from django.urls import path
from .views import MyTokenObtainPairView, CustomLoginView


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
