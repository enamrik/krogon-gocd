from typing import Callable, TypeVar, Union, Tuple, Any

A = TypeVar('A')
B = TypeVar('B')
E = TypeVar('E')

Maybe = Union[Tuple['just', A], Tuple['nothing']]


def just(value=None):
    return "just", value


def nothing():
    return "nothing", None


def map(maybe: Maybe[A], mapper: Callable[[A], B]) -> Maybe[B]:
    if maybe[0] == "just":
        return just(mapper(maybe[1]))
    elif maybe[0] == "nothing":
        return maybe


def from_maybe(maybe: Maybe[A], dict_args: dict) -> B:
    if_just: Callable = dict_args['if_just']
    if_nothing: Callable = dict_args['if_nothing']

    if maybe[0] == "just" and if_just is not None:
        return if_just(maybe[1])
    elif maybe[0] == "nothing" and if_nothing is not None:
        return if_nothing()
    else:
        raise Exception('Invalid Maybe: {}, {}'.format(maybe, dict_args))


def _cast_to_maybe(result):
    if isinstance(result, tuple) and len(result) == 2:
        maybe_type, value = result
        if maybe_type == "just" or maybe_type == "nothing":
            return result
    return "just", result


def nlist(items=None):
    if items is None:
        items = []
    return NullableList(items)


def nmap(map: dict):
    return NullableMap(map)


class NullableList(list):
    def append_if_value(self, value: Maybe[Any]):
        return from_maybe(
            value,
            dict(if_just=lambda val: NullableList(self + [val]),
                 if_nothing=lambda: self))

    def append_if_list(self, value: Maybe[list]):
        return from_maybe(
            value,
            dict(if_just=lambda a_list: NullableList(self + a_list),
                 if_nothing=lambda: self)
        )

    def append(self, value: Any):
        return NullableList(self + [value])

    def to_list(self):
        return list(self)


class NullableMap(dict):
    def get_or_none(self, key: Any):
        return self[key] if key in self else None

    def append_if_value(self, key: Any, value: Maybe):
        return from_maybe(
            value,
            dict(if_just=lambda val: NullableMap(dict(self, **{key: val})),
                 if_nothing=lambda: self))

    def to_map(self):
        return dict(self)
