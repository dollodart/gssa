from gssa.env import global_cache
import json as jsonlib


def cache(data, filename, directory=None):
    if directory is not None:
        filepath = directory.joinpath(filename)
    else:
        filepath = CACHE_DIR.joinpath(filename)
    global_cache.append(filepath)
    with open(filepath, 'w') as _:
        _.write(jsonlib.dumps(data))
    return None


def load_cache(filename, directory=None):
    if directory is not None:
        filepath = directory.joinpath(filename)
    else:
        filepath = CACHE_DIR.joinpath(filename)
    if filepath in global_cache:
        with open(filepath, 'r') as _:
            return jsonlib.load(_)
    return None


def load_cache_paginated(fileprefix, directory=None):
    counter = 1
    data = load_cache(f'{fileprefix}-{counter}', directory)
    queries = []
    # while data := load_cache(f'{fileprefix}-{counter}') is not None: # strange error of only bool results for data
    while data is not None:
        queries.append(data)
        counter += 1
        data = load_cache(f'{fileprefix}-{counter}', directory)
    if queries == []:
        return None
    return queries
