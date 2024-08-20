from django.shortcuts import render
from youtube_transcript_api import YouTubeTranscriptApi
from django.http import HttpResponse
import re

def home(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        video_id = extract_video_id(video_url)
        if video_id:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                return render(request, 'summarizer/result.html', {'transcript': transcript, 'video_url': video_url})
            except Exception as e:
                error_message = str(e)
                if "Subtitles are disabled for this video" in error_message:
                    error_message = "Subtitles are disabled for this video. Please try another video."
                return render(request, 'summarizer/error.html', {'error_message': error_message, 'video_url': video_url})
        else:
            return render(request, 'summarizer/error.html', {'error_message': "Invalid YouTube URL", 'video_url': video_url})
    return render(request, 'summarizer/home.html')

def extract_video_id(url):
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?:@[^\/]+\/)?(.{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"