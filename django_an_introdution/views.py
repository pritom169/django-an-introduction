"""
To render html web pages
"""
from django.http import HttpResponse
HTML_STRING = """
<h1>Hello World</h1>
"""

def home(request):
    """
    Take in a request
    Return HTML as a response
    """
    return HttpResponse(HTML_STRING)