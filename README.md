# yan_image_search_docker

### setup subnetwork for the image search

```bash
docker network create --subnet=172.18.0.0/16 image_search_network
```


### start the vector search docekr

```bash
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

```bash
docker build -t yanliang12/yan_image_search:1.0.1 .

docker run -it \
--net image_search_network \
--ip 172.18.0.22 \
-v /Users/yan/Downloads/:/Downloads/ \
yanliang12/yan_image_search:1.0.1 
```

### code example

```python
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

'''
images/ib_5.png          0.0
images/ib_2.jpg          31450.896484375
images/firstrade_7.png   32310.41796875
images/fab_4.png         33088.15234375
images/ib_6.png          33429.1796875
images/mbzuai_3.png      34033.0546875
images/ib_8.png          34149.71875
images/digital14_1.png   34365.1328125
images/firstrade_2.jpg   35225.5703125
images/kaust_3.png       35914.09375
'''

########query similar image######
```
