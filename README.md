# yan_image_search_docker

```
docker build -t yanliang12/yan_image_search:1.0.1 .

docker run -it \
yanliang12/yan_image_search:1.0.1 
```


### start the vector search docekr

```
sudo docker pull milvusdb/milvus:1.1.0-cpu-d050721-5e559c

export USER=/Users/yan

mkdir -p $USER/milvus/conf
cd $USER/milvus/conf
wget https://raw.githubusercontent.com/milvus-io/milvus/v1.1.0/core/conf/demo/server_config.yaml

sudo docker run -d \
-p 19530:19530 \
-p 19121:19121 \
-v $USER/milvus/db:/var/lib/milvus/db \
-v $USER/milvus/conf:/var/lib/milvus/conf \
-v $USER/milvus/logs:/var/lib/milvus/logs \
-v $USER/milvus/wal:/var/lib/milvus/wal \
milvusdb/milvus:1.1.0-cpu-d050721-5e559c 

sudo docker ps
```
