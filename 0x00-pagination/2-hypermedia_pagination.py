#!/usr/bin/env python3
"""
Calculating start and end index for pagination
"""
import csv
import math
from typing import List, Tuple, Dict, Any


def index_range(page: int, page_size: int) -> Tuple:
    """
    Calculate the start and end index for a given page and page size.

    Args:
        page (int): The page number, 1-indexed.
        page_size (int): The number of items per page.

    Returns:
        tuple: A tuple containing the start and end index.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get a page from the dataset.

        Args:
            page (int): The page number, 1-indexed.
            page_size (int): The number of items per page.

        Returns:
            List[List]: The appropriate page of the dataset.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()
        return (
            dataset[start_index:end_index]
            if start_index < len(dataset) else []
            )

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Get a hypermedia page from the dataset.

        Args:
            page (int): The page number, 1-indexed.
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Any]: A dictionary containing hypermedia pagination details.
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)

        hypermedia = {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages,
        }

        return hypermedia
