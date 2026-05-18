import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FishingLog.settings')

class RealIPMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Cloudflare Tunnel and Nginx pass the real client IP in headers.
        # We extract it and set REMOTE_ADDR so all Django apps and signals see it.
        ip = environ.get('HTTP_CF_CONNECTING_IP') or environ.get('HTTP_X_REAL_IP')
        if ip:
            # Handle possible comma-separated list
            environ['REMOTE_ADDR'] = ip.split(',')[0].strip()
        return self.app(environ, start_response)

application = get_wsgi_application()
application = RealIPMiddleware(application)
