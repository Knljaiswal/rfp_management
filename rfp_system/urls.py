from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create/', views.create_rfp, name='create_rfp'),
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('rfp/<str:rfp_id>/send/', views.send_rfp, name='send_rfp'), # <-- NEW
    path('rfp/<str:rfp_id>/add-proposal/', views.add_proposal, name='add_proposal'),
    path('rfp/<str:rfp_id>/compare/', views.view_proposals, name='view_proposals'),
]