from django.urls import path
from .import views
from apps.public_services.views import add_lost_and_found_item, lost_and_found, pending_items


urlpatterns = [
    path('public_services/', views.public_utilities, name='public_utilities'),
    path('achados-e-perdidos/', views.lost_and_found, name='lost_and_found'),
    path('achados-e-perdidos/adicionar/', add_lost_and_found_item, name='add_lost_and_found'),
    path('download-item/<int:item_id>/', views.download_item, name='download_item'),
    path('pending-items/', pending_items, name='pending_items'),
]
