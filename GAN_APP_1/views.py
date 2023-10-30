from django.shortcuts import render
from django.conf import settings
import tensorflow as tf
from tensorflow import keras
import base64
from io import BytesIO
from .models import Collection


cache_context = {}
    
    
cache_context = {}
    
def home(request):
    if request.method == 'POST':
        if request.POST.get('btn_name') == 'Generate Images':
            fashion_type = request.POST.get('dropdown')

            model = 'generator_model-1.h5'

            # if fashion_type == 'Half T-shirt':
            #     model = 'generator_model_half_sleeves.h5'

            # elif fashion_type == 'Hoddies':
            #     model = 'generator_model_hoodies.h5'

            # elif fashion_type == 'Full T-shirt':
            #     model = 'generator_model_full_sleeves.h5'
            

            # print(fashion_type, model)
            context = generate_images(model)

            # print(fashion_type, model)

            return render(request, 'index.html', context)
            # return render(request, 'index.html')
        
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


def generate_images(model):
    generator = keras.models.load_model(model)

    batch_size = 6
    latent_dim = 128

    random_latent_vectors = tf.random.normal(shape=(batch_size, latent_dim))

    fake = generator(random_latent_vectors)

    image_info = {}

    for i in range(5):
        img = keras.preprocessing.image.array_to_img(fake[i])
        
        buffer = BytesIO()
        
        img.save(buffer, "PNG")
        
        # Encode as base64 and convert to string
        img_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')  

        image_info['img_' + str(i)] = img_bytes


    context = {'image': image_info}

    cache_context = context

    return context


def team(request):
    return render(request, 'teamMembersPage.html')