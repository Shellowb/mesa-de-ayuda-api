from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from bot import views

urlpatterns = [
  path('', csrf_exempt(views.BotView.as_view())),
  # path('chatbot', views.index, name='index'),
  # path('chatbot/<str:room_name>/', views.room, name='room'),
  path('chats/', views.chat_list, name='chats'),
  path('chats/<id_chat>', views.first_message, name='chats'),
]