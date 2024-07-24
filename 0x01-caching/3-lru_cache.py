#!/usr/bin/env python3
""" LIRUCache module """
from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """The least recently used"""

    def __init__(self):
        """Initialize method"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Put method for recently used"""
        if key is not None and item is not None:
            if key in self.cache_data:
                self.cache_data.move_to_end(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded = next(iter(self.cache_data))
                print(f"DISCARD: {discarded}")
                self.cache_data.popitem(last=False)
            self.cache_data[key] = item

    def get(self, key):
        """Get an item from key"""
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
            return self.cache_data[key]
        return
