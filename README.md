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
