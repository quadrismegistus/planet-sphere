from pprint import pprint
import random
import os
from functools import lru_cache as cache, cached_property
from typing import *
# from fastapi import FastAPI
# from sqlmodel import Field, Session, SQLModel, create_engine, select, Column
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy import create_engine, func
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import text as sql_text
from geopy.distance import geodesic
from shapely import wkb
import itertools
from sqlalchemy import and_
import numpy as np
import time
from datetime import datetime
import json
import string
import ipinfo
from base64 import b64decode,b64encode
import plotly.express as px
import pandas as pd

PATH_DATA = os.path.expanduser('~/.cache/flatearth-backend')
PATH_REPO = os.path.dirname(os.path.dirname(__file__))

PATHS_SPATIALITE = ['/opt/homebrew/lib/mod_spatialite.dylib']

DB_USERNAME = 'postgres'
DB_PASSWORD = 'notflat'
DB_DATABASE = 'flatearth'
DB_HOST = 'localhost'
DB_PORT = 5433
DB_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
DB_CMD_PREF = f"PGPASSWORD={DB_PASSWORD} psql -U {DB_USERNAME} -h {DB_HOST} -p {DB_PORT}"
DB_CLEAR = False
IPINFO_TOKEN = '90df1baf7c373a'

NULL_LAT = -68.8333
NULL_LON = -90.5833


MAPBOX_ACCESS_TOKEN_b64=b'cGsuZXlKMUlqb2ljbmxoYm1obGRYTmxjaUlzSW1FaU9pSmpiRzFuYmpGM2NtNHdZV2Q1TTNKelpXOXVibXB3YzJwbEluMC5PQ0ZBVlppa0JHREZTOVRlQ0F6aDB3'
MAPBOX_ACCESS_TOKEN = b64decode(MAPBOX_ACCESS_TOKEN_b64).decode('utf-8')

from .utils import *
