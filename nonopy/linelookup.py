from typing import Generic, Tuple, TypeVar, List

T = TypeVar('T')


class LineLookup(Generic[T]):
    def __init__(self, *, rows: List[T], columns: List[T]):
        self.__lookup = {
            'c': columns,
            'r': rows,
        }

    def __getitem__(self, key: Tuple[str, int]) -> T:
        order, index = key
        return self.__lookup[order][index]

    def __setitem__(self, key: Tuple[str, int], value: T):
        order, index = key
        self.__lookup[order][index] = value

    def __iter__(self):
        return iter(self.__lookup.items())

    rows = property(lambda self: self.__lookup['r'])
    columns = property(lambda self: self.__lookup['c'])