from django.urls import path
from . import views
from .views import ReviewCreateView, ReviewListView

urlpatterns = [
    path('', views.index, name='reviews_index'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('ads/<int:ad_id>/reviews/', ReviewListView.as_view(), name='review-list'),
]
