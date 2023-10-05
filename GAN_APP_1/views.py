from django.shortcuts import render
from pexels_api import API
from django.conf import settings
import requests

# Create your views here.
def home(request):
    return render(request, 'index.html')


def getPhotos(request):
    api  = API(settings.PEXELS_API_KEY)

    endpoint = 'https://api.pexels.com/v1/curated'
    
    images = api.search(endpoint, results_per_page=15)['photos']

    return render(request, 'index.html', {'image': images})
