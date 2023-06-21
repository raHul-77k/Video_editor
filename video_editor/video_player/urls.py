from django.urls import path
from .views import *

app_name = 'video_player'

urlpatterns = [
    path('upload/', UploadVideoView.as_view(), name='video_upload'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('<int:pk>/edit/', EditVideoView.as_view(), name='video_edit'),
    path('<int:pk>/preview/', PreviewVideoView.as_view(), name='video_preview'),
    path('<int:pk>/download/', DownloadVideoView.as_view(), name='video_download'),
]
