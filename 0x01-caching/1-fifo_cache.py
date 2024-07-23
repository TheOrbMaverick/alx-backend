#!/usr/bin/env python3
"""
First In First Out
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    LIFOCache defines a caching system with LIFO eviction policy 
    """

    def __init__(self):
        """Initialize the cache"""
        super().__init__()
        self.last_key = None

    def put(self, key, item):
        """Add an item in the cache"""
        self.cache_data[key] = item
        if key is None or item is None:
            return
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
            if self.last_key is not None:
                print(f"DISCARD: {self.last_key}")
                del self.cache_data[self.last_key]
        self.cache_data[key] = item
        self.last_key = key

    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key, None)
