from typing import get_origin
import inspect


def check_types(func: callable):

    def wrapped(*args, **kwargs):
        sig = inspect.signature(func)
        given_args = sig.bind(*args, **kwargs).arguments

        expected_types = func.__annotations__
        for arg in expected_types:
            if arg != 'return' and get_origin(sig.parameters[arg].annotation):
                expected_types[arg] = get_origin(sig.parameters[arg].annotation)

        for arg, val in given_args.items():
            if not isinstance(val, expected_types[arg]):
                raise TypeError(f'Incorrect argument {arg}: expected type {expected_types[arg].__name__}, '
                                    f'got type {type(val).__name__}')

        if 'return' in expected_types:
            result = func(*args, **kwargs)
            return_type = expected_types['return']
            if not isinstance(result, return_type):
                raise TypeError(f'Incorrect return: expected type {return_type.__name__}, '
                                f'got type {type(result).__name__}')

        return func(*args, **kwargs)

    return wrapped


@check_types
def func1(a: int, b: str) -> str:
    return a * b


# print(func1(2, 'hi hello '))  # hi hello hi hello
# print(func1(2, 2))  # TypeError: Argument b: expected type str, got type int


@check_types
def func2(a: list[list[list]], b: list[int]):
    return a + b


# print(func2(tuple([]), []))  # TypeError: incorrect argument a: expected type list, got type tuple
# print(func2([1], [2]))  # [1, 2]


@check_types
def func3(a: list, b: list[list[list[dict]]]) -> int:
    return 4


# print(func3(['a'], ['3', 3]))  # TypeError: Incorrect return: expected type int, got type list
# print(func3(b=[], a=tuple()))  # TypeError: Incorrect argument a: expected type list, got type tuple
# print(func3([1, 2, 3], ['a' * 10]))  # 4
