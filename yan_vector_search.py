from milvus import *

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



image_pathes = [
'digital14_1.png',
'digital14_2.jpg',
'digital14_3.jpg',
'mbzuai_1.png',
'mbzuai_2.jpg',
'mbzuai_3.png',
'mbzuai_4.jpg',
'darkmatter1.png',
'darkmatter2.png',
'g421.png',
'g423.png',
'g422.jpg',
'iiai1.jpg',
'iiai2.png',
'iiai3.png',
]

image_mata = {}

for i in image_pathes:
	vector = yan_image_embedding.image_to_vector(i)
	result = milvus.insert(collection_name='image', records=[vector])
	image_id = result[1][0]
	image_path = i
	image_mata[image_id] = image_path

milvus.count_entities(collection_name='image')
########build the collection#########





########query similar image######

queyr_image = 'digital14_3.jpg'
vector = yan_image_embedding.image_to_vector(queyr_image)

search_param = {'nprobe': 16}
search_result = milvus.search(collection_name='image', query_records=[vector], top_k = 100, params=search_param)

for r in search_result[1][0]:
	print(image_mata[r.id], '\t',r.distance)

########query similar image######