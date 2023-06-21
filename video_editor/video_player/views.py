from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse, JsonResponse
from .forms import VideoForm
from .models import Video
import moviepy.editor as mp
from moviepy.editor import *
from django.contrib import messages
from tempfile import NamedTemporaryFile
import os
from django.conf import settings
from django.core.files import File


class UploadVideoView(View):
    template_name = 'upload_video.html'
    form_class = VideoForm
    success_url = reverse_lazy('video_player:video_detail')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)

            # Save the uploaded file to a temporary file
            with NamedTemporaryFile(delete=False) as f:
                f.write(video.video_file.read())
                video_filename = f.name
            with NamedTemporaryFile(delete=False) as f:
                f.write(video.thumbnail.read())
                thumbnail_filename = f.name

            # Process the video
            clip = mp.VideoFileClip(video_filename)
            clip = clip.resize(height=360)
            clip = clip.fx(mp.vfx.fadeout, duration=1)

            # Add text and image to the video
            txt_clip = (mp.TextClip("Hello World", fontsize=70, color='white')
                        .set_position('center')
                        .set_duration(clip.duration))
            img_clip = (mp.ImageClip(thumbnail_filename)
                        .set_duration(clip.duration)
                        .resize(height=50)
                        .set_position(('right','bottom')))
            final_clip = mp.CompositeVideoClip([clip, txt_clip, img_clip])

            # Save the processed video and thumbnail
            with open(video.video_file.path, 'wb+') as destination:
                for chunk in video.video_file.chunks():
                    destination.write(chunk)
            final_clip.write_videofile(video.video_file.path)
            
            with open(video.thumbnail.path, 'wb+') as destination:
                for chunk in video.thumbnail.chunks():
                    destination.write(chunk)
            final_clip.save_frame(video.thumbnail.path)
            
            # Save the video to the database
            video.save()

            messages.success(request, 'Video uploaded successfully.')
            return redirect(self.success_url, pk=video.pk)


class VideoDetailView(View):
    template_name = 'video_details.html'

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        return render(request, self.template_name, {'video': video})


class DownloadVideoView(View):
    def get(self, request, pk):
        video = Video.objects.get(pk=pk)
        file_path = video.video_file.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename=' + video.title + '.mp4'
            return response


class EditVideoView(View):
    model = Video
    form_class = VideoForm
    template_name = 'video_player/video_edit.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('video_player:video_detail', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        # Implement GET method logic here
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Implement POST method logic here
        return super().post(request, *args, **kwargs)



    def get_preview_clip(self, file_path):
        video = mp.VideoFileClip(file_path)
        preview_clip = video.subclip(0, 5)  # preview only the first 5 seconds
        video.reader.close()
        video.audio.reader.close_proc()
        return preview_clip


class PreviewVideoView(View):
    def get(self, request, pk):
        video = get_object_or_404(Video, id=pk)
        video_path = video.video_file.path
        preview_clip = VideoFileClip(video_path).subclip(0, 5)
        preview_filename = f'{video.title}_preview.mp4'
        preview_dir = os.path.join(settings.MEDIA_ROOT, 'previews')
        preview_path = os.path.join(preview_dir, preview_filename)

        # Create previews directory if it doesn't exist
        if not os.path.exists(preview_dir):
            os.makedirs(preview_dir)

        preview_clip.write_videofile(preview_path, fps=24)
        return JsonResponse({'success': True})