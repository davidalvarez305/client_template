from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>', views.category, name='category'),
    path('single/<slug:slug>', views.review_post, name='review_post')
]