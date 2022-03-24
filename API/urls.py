from django.urls import path
from . import views
from .routes.admins import admin_login, manage_admins
from .routes.products import manage_products
from .routes.sales import manage_sales
from .routes.events import manage_events

urlpatterns = [
    path('', views.hello_world),
    path('chipottle-admin-login', admin_login, name="AdminLogin"),
    path('chipottle/manage-admins', manage_admins, name="AdminManagers"),
    path('chipottle/manage-admins/<int:pk>', manage_admins, name="AdminManagers"),
    path('chipottle/products', manage_products, name="ManageProducts"),
    path('chipottle/products/<int:pk>', manage_products,),
    path('chipottle/sales', manage_sales),
    path('chipottle/sales/<int:pk>', manage_sales),
    path('chipottle/events', manage_events),
    path('chipottle/events/<int:pk>', manage_events),
]