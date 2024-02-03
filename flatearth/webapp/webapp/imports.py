from __future__ import annotations
from typing import Callable
import json
import asyncio
import plotly.graph_objects as go

## import logic
import os,sys
path_repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if not sys.path or sys.path[0]!=path_repo:
    sys.path.insert(0,path_repo)
from flatearth import *
###

import reflex as rx

DARK_MODE_DEFAULT = False



##
from . import styles
from . import scripts
from .states import *
from .templates import template
