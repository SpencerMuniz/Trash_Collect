from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('confirm_pickup_charge_balance/<int:customer_id>', views.confirm_pickup_charge_balance, name="confirm_pickup_charge_balance"),
    path('search_weekday_pickup/', views.search_weekday_pickup, name="search_weekday_pickup")
]