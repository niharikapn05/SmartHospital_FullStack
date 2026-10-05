from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def linear_search(
    items: list[T],
    condition: Callable[[T], bool]
) -> T | None:

    for item in items:
        if condition(item):
            return item

    return None


def filter_items(
    items: list[T],
    condition: Callable[[T], bool]
) -> list[T]:

    return [item for item in items if condition(item)]


def sort_by_name(items: list[T], key: Callable[[T], str]) -> list[T]:

    return sorted(items, key=key)


def binary_search(
    items: list[T],
    target: str,
    key: Callable[[T], str]
) -> T | None:

    left = 0
    right = len(items) - 1

    while left <= right:

        middle = (left + right) // 2
        value = key(items[middle])

        if value.lower() == target.lower():
            return items[middle]

        if value.lower() < target.lower():
            left = middle + 1
        else:
            right = middle - 1

    return None