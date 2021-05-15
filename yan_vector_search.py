import numpy
from milvus import *
from os import listdir
from os.path import isfile, join
import yan_image_embedding


milvus = Milvus(host='172.18.0.20', port='19530')


########build the collection#########

try:
	milvus.drop_collection(collection_name='image')
except:
	pass

param = {'collection_name':'image', 'dimension':4096, 'index_file_size':1024, 'metric_type':MetricType.L2}
milvus.create_collection(param)
milvus.list_collections()

image_files = [join('images', f) for f in listdir('images') if isfile(join('images', f))]
image_mata = {}

for i in image_files:
	try:
		print('\n\nextracting features from {}'.format(i))
		vector = yan_image_embedding.image_to_vector(i)
		print('inserting feature vector to collection')
		result = milvus.insert(collection_name='image', records=[vector])
		image_id = result[1][0]
		image_path = i
		image_mata[image_id] = image_path
	except Exception as e:
		print(e)

milvus.count_entities(collection_name='image')
########build the collection#########





########query similar image######
queyr_image = join('images', 'ib_5.png')
vector = yan_image_embedding.image_to_vector(queyr_image)
search_result = milvus.search(collection_name='image', query_records=[vector], top_k = 10, params={'nprobe': 16})

for r in search_result[1][0]:
	print(image_mata[r.id], '\t',r.distance)
########query similar image######