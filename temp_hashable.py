#!/usr/bin/env python3
from __future__ import print_function
from typing import Hashable


class TempHashable:
    """
    A utility class that allows objects that don't normally support
    hashing to be hashed, making things like deduplicating
    a list of dictionaries possible
    """
    def __init__(self, obj):
        self._original_obj = obj
        self._hashable_obj = TempHashable.make_hashable(obj)

    def restore(self):
        return self._original_obj

    def __hash__(self):
        return hash(self._hashable_obj)

    def __eq__(self, other):
        return self._hashable_obj == other

    def __ne__(self, other):
        return self._hashable_obj != other

    def __gt__(self, other):
        try:
            return self._hashable_obj > other
        except TypeError:
            tmp = TempHashable.make_hashable(other)
            return hash(self._hashable_obj) > hash(tmp)

    def __ge__(self, other):
        try:
            return self._hashable_obj >= other
        except TypeError:
            tmp = TempHashable.make_hashable(other)
            return hash(self._hashable_obj) >= hash(tmp)

    def __lt__(self, other):
        try:
            return self._hashable_obj < other
        except TypeError:
            tmp = TempHashable.make_hashable(other)
            return hash(self._hashable_obj) < hash(tmp)

    def __le__(self, other):
        try:
            return self._hashable_obj <= other
        except TypeError:
            tmp = TempHashable.make_hashable(other)
            return hash(self._hashable_obj) <= hash(tmp)

    def __iter__(self):
        return iter(self._hashable_obj)

    @staticmethod
    def make_hashable(obj):

        if isinstance(obj, Hashable):
            return obj
        elif isinstance(obj, list):
            return tuple(obj)
        elif isinstance(obj, set):
            # set has to be sorted to make sure __eq__ runs correctly for it
            # but each element already must be hashable to be in the list,
            # so no need to process each item individually
            hashable_list = list(obj)
            hashable_list.sort()
            return tuple(hashable_list)
        elif isinstance(obj, dict):
            # dicts need each value to be confirmed as hashable, but keys
            # already have to be hashable
            hashable_dict = [(k, TempHashable.make_hashable(v))
                             for k, v in obj.items()]
            # sort by dict key to make sure that changes to the values don't
            # break sort order
            hashable_dict.sort(key=lambda a: a[0])
            return tuple(hashable_dict)
        return obj


def main():
    list_of_dicts = [
        {"a": 1},
        {"a": 1},
        {"a": {"b": 1}},
        {"a": "b"}
    ]

    hashable_objs = [TempHashable(o) for o in list_of_dicts]
    deduped_hashable = list(set(hashable_objs))
    deduped_hashable.sort()

    deduped = [o.restore() for o in deduped_hashable]

    for i in deduped:
        print("%s" % str(i))


if __name__ == "__main__":
    main()
