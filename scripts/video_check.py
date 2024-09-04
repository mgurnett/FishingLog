from catches.models import Video
import requests

bad_vids = []

def check_video_url(video_url, video_id):

    request = requests.get(video_url)
    if "Video unavailable" in request.text:
        bad_vids.append(video_id)
        return str('\x1b[205;49;49m' + 'Video unavailable' + '\x1b[0m')
    else:
        return str('\x1b[6;30;42m' + 'Video checked' + '\x1b[0m')
    
def run():
    videos = Video.objects.all()
    total = len(videos)
    for index, video in enumerate(videos):
        result = check_video_url (video.url, video.id)

        print (f'{total - index} - {video.name = } {result}')
        # print (result)
    print (f'The list of bad videos is: {bad_vids}')
