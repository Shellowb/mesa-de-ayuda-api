from django.urls import path
from process import views

urlpatterns = [
  path('', views.process_list),
  path('publicados', views.process_list_published),
  path('<id_process>', views.process_detail),
]