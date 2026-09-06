import os
import urllib.request
import urllib.parse
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_picture_download_dir():
    path = os.path.join(settings.BASE_DIR, 'public', 'downloads', 'picture')
    os.makedirs(path, exist_ok=True)
    return path

def get_article_download_dir():
    path = os.path.join(settings.BASE_DIR, 'public', 'downloads', 'article')
    os.makedirs(path, exist_ok=True)
    return path

def download_picture_from_url(url, name=""):
    """
    Downloads image from external URL, saves a copy to /public/downloads/picture/
    and returns (ContentFile, local_filepath).
    """
    download_dir = get_picture_download_dir()
    
    parsed = urllib.parse.urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']:
        ext = '.jpg'
    
    base_name = slugify(name) if name else os.path.splitext(os.path.basename(parsed.path))[0]
    if not base_name:
        base_name = 'downloaded_picture'
    
    filename = f"{base_name}{ext}"
    local_path = os.path.join(download_dir, filename)
    
    # Handle filename collisions in downloads folder
    counter = 1
    while os.path.exists(local_path):
        filename = f"{base_name}_{counter}{ext}"
        local_path = os.path.join(download_dir, filename)
        counter += 1

    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        content_type = response.headers.get('Content-Type', '')
        if 'png' in content_type and not filename.endswith('.png'):
            filename = os.path.splitext(filename)[0] + '.png'
            local_path = os.path.join(download_dir, filename)
        elif ('jpeg' in content_type or 'jpg' in content_type) and not (filename.endswith('.jpg') or filename.endswith('.jpeg')):
            filename = os.path.splitext(filename)[0] + '.jpg'
            local_path = os.path.join(download_dir, filename)
        elif 'webp' in content_type and not filename.endswith('.webp'):
            filename = os.path.splitext(filename)[0] + '.webp'
            local_path = os.path.join(download_dir, filename)

        data = response.read()

    # Save to /public/downloads/picture/
    with open(local_path, 'wb') as f:
        f.write(data)

    content_file = ContentFile(data, name=filename)
    return content_file, local_path

def download_article_from_url(url, name=""):
    """
    Downloads article or document from external URL, saves a copy to /public/downloads/article/
    and returns (ContentFile, local_filepath).
    """
    download_dir = get_article_download_dir()
    
    parsed = urllib.parse.urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lower()
    if ext not in ['.pdf', '.doc', '.docx', '.txt', '.html', '.htm', '.epub']:
        ext = '.pdf' if '.pdf' in url.lower() else '.html'

    base_name = slugify(name) if name else os.path.splitext(os.path.basename(parsed.path))[0]
    if not base_name:
        base_name = 'downloaded_article'

    filename = f"{base_name}{ext}"
    local_path = os.path.join(download_dir, filename)

    # Handle collisions
    counter = 1
    while os.path.exists(local_path):
        filename = f"{base_name}_{counter}{ext}"
        local_path = os.path.join(download_dir, filename)
        counter += 1

    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        content_type = response.headers.get('Content-Type', '')
        if 'pdf' in content_type and not filename.endswith('.pdf'):
            filename = os.path.splitext(filename)[0] + '.pdf'
            local_path = os.path.join(download_dir, filename)
        elif 'html' in content_type and not (filename.endswith('.html') or filename.endswith('.htm')):
            filename = os.path.splitext(filename)[0] + '.html'
            local_path = os.path.join(download_dir, filename)

        data = response.read()

    # Save to /public/downloads/article/
    with open(local_path, 'wb') as f:
        f.write(data)

    content_file = ContentFile(data, name=filename)
    return content_file, local_path
