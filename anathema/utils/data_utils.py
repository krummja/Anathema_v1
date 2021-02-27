from __future__ import annotations

from typing import Callable, Iterable, Any


def get_first(iterable: Iterable, condition = lambda x : True):
    return next((x for x in iterable if condition(x)), None)

def get_first_key(dictionary, condition):
    matches = []
    for k, v in dictionary.items():
        if v == condition:
            matches.append(k)
    return matches[0] if len(matches) > 0 else None
