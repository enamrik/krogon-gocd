from typing import Callable, TypeVar, Tuple, Union

A = TypeVar('A')
Ap = TypeVar('Ap')
E = TypeVar('E')
Ep = TypeVar('Ep')

Either = Union[Tuple['success', A], Tuple['failure', E]]


def success(value=None):
    return "success", value


def failure(error):
    return "failure", error


def on(either: Either[A, E], dict_args: dict) -> Either[A, E]:
    success_f: Callable = dict_args['success'] if 'success' in dict_args else (lambda _: {})
    failure_f: Callable = dict_args['failure'] if 'failure' in dict_args else (lambda _: {})
    whatever_f: Callable = dict_args['whatever'] if 'whatever' in dict_args else (lambda _v, _e: {})

    if either[0] == "success":
        success_f(either[1])
        whatever_f(either[1], None)
    elif either[0] == "failure":
        failure_f(either[1])
        whatever_f(None, either[1])
    else:
        raise Exception('Invalid Either: {}'.format(either))

    return either


def then(either: Either[A, E], func: Callable[[A], Either[Ap, E]]) -> Either[Ap, E]:
    if either[0] == "success":
        return _cast_to_either(func(either[1]))
    elif either[0] == "failure":
        return either
    else:
        raise Exception('Invalid Either: {}'.format(either))


def _cast_to_either(result):
    if isinstance(result, tuple) and len(result) == 2:
        either_type, value = result
        if either_type == "success" or either_type == "failure":
            return result
    return "success", result


def catch_error(either: Either[A, E], func: Callable[[E], Either[Ap, Ep]]) -> Either[Ap, Ep]:
    if either[0] == "success":
        return either
    elif either[0] == "failure":
        return _cast_to_either(func(either[1]))
    else:
        raise Exception('Invalid Either: {}'.format(either))
