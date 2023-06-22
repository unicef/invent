from django.conf import settings


class InternalIPsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip not in settings.INTERNAL_IPS:
            # Add Docker container's IP to INTERNAL_IPS
            settings.INTERNAL_IPS.append(ip)
        response = self.get_response(request)
        print(f'dev response: {response}')
        return response
