from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import RequestLog, BlockedIP
import requests

class IPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Task 1: Check Blacklist
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blacklisted.")

        # Task 2: Geolocation with 24h Caching
        geo_data = cache.get(f'geo_{ip}')
        if not geo_data:
            try:
                # Using a free API (you can replace with django-ipgeolocation logic)
                response = requests.get(f'https://ipapi.co/{ip}/json/').json()
                geo_data = {
                    'country': response.get('country_name'),
                    'city': response.get('city')
                }
                cache.set(f'geo_{ip}', geo_data, 86400) # 24 hours
            except:
                geo_data = {'country': None, 'city': None}

        # Task 0: Log Request
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=geo_data.get('country'),
            city=geo_data.get('city')
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
