###############yan_image_embedding.py##############

from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.models import Model
import numpy as np

base_model = VGG19(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

def image_to_vector(img_path):
	img = image.load_img(img_path, target_size=(224, 224))
	x = image.img_to_array(img)
	x = np.expand_dims(x, axis=0)
	x = preprocess_input(x)
	features = model.predict(x)[0].tolist()
	return features


'''
wget https://m.eyeofriyadh.com/news_images/2020/01/1f75d29d39631.jpg

vector = image_to_vector('1f75d29d39631.jpg')
'''

###############yan_image_embedding.py##############