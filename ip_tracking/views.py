from ratelimit.decorators import ratelimit
from django.http import JsonResponse
from django.contrib.auth import authenticate

@ratelimit(key='ip', rate='5/m', block=True) # Anonymous
@ratelimit(key='user', rate='10/m', block=True) # Authenticated logic simplified
def login_view(request):
    return JsonResponse({"message": "Login endpoint"})
