from django.shortcuts import render
from pexels_api import API
from django.conf import settings
import tensorflow as tf
from tensorflow import keras
import base64
from io import BytesIO
    

def generate_images(request):
    generator = keras.models.load_model("generator_model.h5")

    batch_size = 7
    latent_dim = 128

    random_latent_vectors = tf.random.normal(shape=(batch_size, latent_dim))

    fake = generator(random_latent_vectors)

    image_info = {}

    for i in range(4):
        img = keras.preprocessing.image.array_to_img(fake[i])
        
        buffer = BytesIO()
        
        img.save(buffer, "PNG")
        
        # Encode as base64 and convert to string
        img_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')  

        image_info['img_' + str(i)] = img_bytes


    context = {'image': image_info}

    return render(request, 'index.html', context)


def getPhotos(request):
    api  = API(settings.PEXELS_API_KEY)

    endpoint = 'https://api.pexels.com/v1/curated'
    
    images = api.search(endpoint, results_per_page = 10)['photos']

    return render(request, 'index.html', {'image': images})
