from __future__ import annotations
from typing import Callable
import json

## import logic
import os,sys
path_repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if not sys.path or sys.path[0]!=path_repo:
    sys.path.insert(0,path_repo)
import round_earth
###

import reflex as rx



##
from . import styles
from .state import *
from .templates import template
