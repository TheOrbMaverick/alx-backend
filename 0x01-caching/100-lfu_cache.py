#!/usr/bin/env python3
""" LFUCache module """

from base_caching import BaseCaching
from collections import defaultdict


class LFUCache(BaseCaching):
    """ LFUCache defines a caching system with LFU eviction policy """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.frequency = defaultdict(int)
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lfu_keys = [
                    k for k,
                    v in self.frequency.items()
                    if v == min(self.frequency.values())
                    ]
                lru_lfu_key = min(lfu_keys, key=lambda k: self.order.index(k))
                print(f"DISCARD: {lru_lfu_key}")
                del self.cache_data[lru_lfu_key]
                del self.frequency[lru_lfu_key]
                self.order.remove(lru_lfu_key)

            self.cache_data[key] = item
            self.frequency[key] = 1
            self.order.append(key)

    def get(self, key):
        """ Get an item by key """
        if key in self.cache_data:
            self.frequency[key] += 1
            self.order.remove(key)
            self.order.append(key)
            return self.cache_data[key]
        return None
