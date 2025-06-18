from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shipment_prediction/', views.shipment_prediction, name='shipment_prediction'),
    path('demand_forecasting/', views.demand_forecasting, name='demand_forecasting'),
    path('inventory_optimization/', views.inventory_optimization, name='inventory_optimization'),
    path('agent/', views.agent_query, name='agent_query'),
]
