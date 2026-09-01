import time 

_cache = {}

def get(key:str, max_age: int = 3600):
    """ Cache'den verial. max_age saniye cinsinden."""
    if key in _cache:
        data, timestamp = _cache[key]
        if time.time() - timestamp < max_age:
            return data

    return None

def set(key:str, data):
    """ Cache'e veri yaz."""
    _cache[key] = (data,time.time())
