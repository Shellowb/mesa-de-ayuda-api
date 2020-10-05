from django.urls import path
from instances import views

urlpatterns = [
  path('', views.instance_list),
  path('etapas', views.steps_list),
  path('etapas/<id_step>', views.steps_detail),
  path('novedades', views.news_list),
  path('novedades/<id_news>', views.news_detail),
  path('publicados', views.instance_list_published),
  path('<id_instance>', views.instance_detail),
  path('<id_instance>/etapas', views.instance_list_steps),
  path('<id_instance>/novedades', views.instance_list_news),
  path('<id_process>/instancias', views.process_list_instances),
]