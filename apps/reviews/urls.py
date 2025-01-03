from django.urls import path, include
from . import views


urlpatterns = [ 
    path('', views.list_reviews, name='reviews'),
    #path('reviews', views.reviews_detail, name='restaurant_details'),
]
