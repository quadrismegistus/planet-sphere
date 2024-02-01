# flatearth
Towards a new public sphere


## Backend


### Install

#### Docker setup

```
docker run -d \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=notflat \
  -p 5433:5432 \
  --name flatearth-postgis \
  postgis/postgis
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



## Attribution

* Icons
  * darkmode by Tim Rostilov from <a href="https://thenounproject.com/browse/icons/term/darkmode/" target="_blank" title="darkmode Icons">Noun Project</a> (CC BY 3.0)