from milvus import *

milvus = Milvus(host='172.18.0.20', port='19530')

try:
  milvus.drop_collection(collection_name='uae_company_logo')
except:
  pass

param = {'collection_name':'uae_company_logo', 'dimension':4096, 'index_file_size':1024, 'metric_type':MetricType.L2}
milvus.create_collection(param)
milvus.list_collections()

image_pathes = [
'/Downloads/digital14_1.png',
'/Downloads/digital14_2.jpg',
'/Downloads/digital14_3.jpg',
'/Downloads/mbzuai_1.png',
'/Downloads/mbzuai_2.jpg',
'/Downloads/mbzuai_3.png',
'/Downloads/mbzuai_4.jpg',
'/Downloads/darkmatter1.png',
'/Downloads/darkmatter2.png',
'/Downloads/g421.png',
'/Downloads/g423.png',
'/Downloads/g422.jpg',
'/Downloads/iiai1.jpg',
'/Downloads/iiai2.png',
'/Downloads/iiai3.png',
]

image_mata = {}

for i in image_pathes:
	vector = image_to_vector(i)
	result = milvus.insert(collection_name='uae_company_logo', records=[vector])
	print(result)
	image_id = result[1][0]
	image_path = i
	image_mata[image_id] = image_path

milvus.count_entities(collection_name='uae_company_logo')


##############

queyr_image = '/Downloads/mbzuai_1.png'
vector = image_to_vector(queyr_image)

search_param = {'nprobe': 16}
search_result = milvus.search(collection_name='uae_company_logo', query_records=[vector], top_k = 100, params=search_param)

for r in search_result[1][0]:
	print(image_mata[r.id], r.distance)
