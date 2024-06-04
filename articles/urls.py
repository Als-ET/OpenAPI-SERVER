from django.urls import path
from .views import query_view, send_message_view, summarize_and_send_news

urlpatterns = [
    path('api/query/', query_view, name='query_view'),
    path('api/send-message/', send_message_view, name='send_message_view'),
    path('api/summarize-and-send-news/', summarize_and_send_news, name='summarize_and_send_news'),
]
