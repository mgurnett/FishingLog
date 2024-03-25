from catches.models import Video
import requests

def check_video_url(video_url):

    request = requests.get(video_url)
    if "Video unavailable" in request.text:
        return str('\x1b[205;49;49m' + 'Video unavailable' + '\x1b[0m')
    else:
        return str('\x1b[6;30;42m' + 'Video checked' + '\x1b[0m')
    
def run():
    videos = Video.objects.all()
    total = len(videos)
    for index, video in enumerate(videos):
        result = check_video_url (video.url)

        print (f'{total - index} - {video.name = }')
        print (result)
