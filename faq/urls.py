from django.urls import path
from faq import views

urlpatterns = [
  path('', views.faq_list),
  path('publicados', views.faq_list_published),
  path('<id_faq>', views.faq_detail),
  path('<id_faq>/like', views.like_faq),
  path('<id_faq>/dislike', views.dislike_faq),
  path('<id_process>/questions', views.process_list_faq),
  path('<id_process>/questions/published', views.process_published_list_faq),
  
]