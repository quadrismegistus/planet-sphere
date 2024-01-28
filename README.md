# round earth
Towards a new public sphere


## Backend


### Install

#### Docker setup

```
docker run -d \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=notflat \
  -p 5433:5432 \
  --name round-earth-postgis \
  postgis/postgis

docker run -d \
  -e PBF_URL=https://download.geofabrik.de/europe/monaco-latest.osm.pbf \
  -e REPLICATION_URL=https://download.geofabrik.de/europe/monaco-updates/ \
  -p 8411:8080 \
  --name round-earth-nominatim \
  mediagis/nominatim:4.3

```

#### Python

```
# install python
pyenv install 3.12.1

# install repo
python -m venv venv
. venv/bin/activate
pip install -e .

```
