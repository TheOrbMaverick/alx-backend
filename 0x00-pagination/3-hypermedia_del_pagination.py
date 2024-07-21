#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Any

class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict[str, Any]:
        """
        Get a hypermedia page from the dataset with a given start index and page size.

        Args:
            index (int): The start index of the page.
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Any]: A dictionary containing hypermedia pagination details.
        """
        assert index is None or (isinstance(index, int) and 0 <= index < len(self.dataset())), \
            "index must be a valid integer within the range of the dataset"

        dataset = self.indexed_dataset()
        data = []
        current_index = index if index is not None else 0
        next_index = current_index

        while len(data) < page_size and next_index < len(self.dataset()):
            if next_index in dataset:
                data.append(dataset[next_index])
            next_index += 1

        hypermedia = {
            "index": index if index is not None else 0,
            "next_index": next_index,
            "page_size": len(data),
            "data": data,
        }
        return hypermedia
