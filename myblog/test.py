import time
from collections import OrderedDict
import functools


class LRUCacheDict:
    def __init__(self, max_size=1024, expiration=60):
        self.max_size = max_size
        self.expiration = expiration

        self._cache = {}
        self._access_records = OrderedDict()
        self._expire_records = OrderedDict()

    def __setitem__(self, key, value):
        now = int(time.time())
        self.__delete__(key)

        self._cache[key] = value
        self._expire_records[key] = now + self.expiration
        self._access_records[key] = now

        self.cleanup()

    def __getitem__(self, item):
        now = int(time.time())
        del self._access_records[item]
        self._access_records[item] = now
        self.cleanup()

        return self._cache[item]

    def __contains__(self, item):
        self.cleanup()
        return item in self._cache

    def __delete__(self, instance):
        if instance in self._cache:
            del self._cache[instance]
            del self._expire_records[instance]
            del self._access_records[instance]

    def cleanup(self):
        if self.expiration is None:
            return None

        pending_delete_keys = []
        now = int(time.time())
        for k, v in self._expire_records.items():
            if v < now:
                pending_delete_keys.append(k)

        for del_k in pending_delete_keys:
            self.__delete__(del_k)

        while len(self._cache) > self.max_size:
            for k in self._access_records:
                self.__delete__(k)
                break


def cache_it(max_size=1024, expiration=60):
    CACHE = LRUCacheDict(max_size=max_size, expiration=expiration)

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            key = repr(*args, **kwargs)
            try:
                result = CACHE[key]
            except KeyError:
                result = func(*args, **kwargs)
                CACHE[key] = result
            return result
        return inner
    return wrapper


@cache_it(max_size=10, expiration=3)
def query(sql):
    time.sleep(1)
    result = "execute %s" % sql
    return result


if __name__ == "__main__":
    print(query("hello"))
    print(query("hello"))
    print(query("world"))

    # cache_dict = LRUCacheDict(max_size=2, expiration=10)
    # cache_dict["name"] = "oliver"
    # cache_dict["age"] = 27
    # cache_dict["addr"] = "shenzhen"
    #
    # print("name" in cache_dict)
    # print("age" in cache_dict)
    #
    # time.sleep(11)
    #
    # print("age" in cache_dict)






























































