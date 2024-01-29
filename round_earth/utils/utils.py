from ..imports import *


def merge_dicts(*ld):
    od = {}
    for d in ld:
        for k in d:
            if not k in od or d[k]:
                od[k] = d[k]
    return od


def first(l, default=None):
    for x in l:
        return x
    return default
