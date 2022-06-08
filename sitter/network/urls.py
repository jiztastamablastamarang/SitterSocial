from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import Feed, VoteView

app_name = 'network'

urlpatterns = [
    path('', csrf_exempt(Feed.as_view()), name='feed'),
    path('vote/<int:pk>', csrf_exempt(VoteView), name='votes'),
]