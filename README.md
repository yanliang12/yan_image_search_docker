# yan_image_search_docker

```
docker network create --subnet=172.18.0.0/16 image_search_network
```


### start the vector search docekr

```

sudo docker pull milvusdb/milvus:1.1.0-cpu-d050721-5e559c

export USER=/Users/yan

rm -r $USER/milvus/conf
mkdir -p $USER/milvus/conf
cd $USER/milvus/conf
wget https://raw.githubusercontent.com/milvus-io/milvus/v1.1.0/core/conf/demo/server_config.yaml
chmod 777 $USER/milvus/conf
chmod 777 $USER/milvus/conf/*

sudo docker run -d \
-p 19530:19530 \
-p 19121:19121 \
-v $USER/milvus/db:/var/lib/milvus/db \
-v $USER/milvus/conf:/var/lib/milvus/conf \
-v $USER/milvus/logs:/var/lib/milvus/logs \
-v $USER/milvus/wal:/var/lib/milvus/wal \
--net image_search_network \
--ip 172.18.0.20 \
milvusdb/milvus:1.1.0-cpu-d050721-5e559c 

sudo docker ps
```

#### build the query service

```
docker build -t yanliang12/yan_image_search:1.0.1 .

docker run -it \
--net image_search_network \
--ip 172.18.0.22 \
-v /Users/yan/Downloads/:/Downloads/ \
yanliang12/yan_image_search:1.0.1 
```

### code example

```python
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

'''
digital14_3.jpg          0.0
digital14_2.jpg          1991.7869873046875
digital14_1.png          15433.568359375
darkmatter1.png          18634.1796875
mbzuai_2.jpg     20856.8984375
mbzuai_3.png     22268.10546875
mbzuai_1.png     25805.171875
darkmatter2.png          27981.859375
g422.jpg         31794.83984375
mbzuai_4.jpg     33009.6171875
g423.png         38055.2421875
g421.png         50007.015625
'''

########query similar image######
```
