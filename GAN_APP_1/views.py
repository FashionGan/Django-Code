from django.shortcuts import render, redirect, HttpResponse
from pexels_api import API
from django.conf import settings
import tensorflow as tf
from tensorflow import keras
import base64
from io import BytesIO
from .models import Collection

cache_context = {}
    
def home(request):
    if request.method == 'POST':
        if request.POST.get('btn_name') == 'Generate Images':
            context = generate_images()

            return render(request, 'index.html', context)
        
        elif request.POST.get('btn_name') == 'add_to_collection':
            image_name = request.POST.get('image_string')

            collection_obj = Collection(image_bytes = image_name)
            collection_obj.save()

            return render(request, 'index.html')
    
    return render(request, 'index.html')

def getCollection(request):
    ls = Collection.objects.all().values()

    context = {'image': ls}

    return render(request, 'collection.html', context = context)


def generate(request):
    return render (request, 'image_page.html')


def generate_images():
    generator = keras.models.load_model("generator_model-1.h5")

    batch_size = 5
    latent_dim = 128

    random_latent_vectors = tf.random.normal(shape=(batch_size, latent_dim))

    fake = generator(random_latent_vectors)

    image_info = {}

    for i in range(1):
        img = keras.preprocessing.image.array_to_img(fake[i])
        
        buffer = BytesIO()
        
        img.save(buffer, "PNG")
        
        # Encode as base64 and convert to string
        img_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')  

        image_info['img_' + str(i)] = img_bytes


    context = {'image': image_info}

    cache_context = context

    return context


def getPhotos(request):
    api  = API(settings.PEXELS_API_KEY)

    endpoint = 'https://api.pexels.com/v1/curated'
    
    images = api.search(endpoint, results_per_page = 10)['photos']

    return render(request, 'index.html', {'image': images})


def team(request):
    return render(request, 'teamMembersPage.html')