from django.urls import path
from category import views

urlpatterns = [
  path('', views.category_list),
  path('<id_category>', views.category_detail),
  path('<id_process>/categories', views.process_list_categories),
]