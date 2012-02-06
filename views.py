# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, world. You're at the poll index.")
