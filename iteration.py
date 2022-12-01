from typing import Any, TypeVar
from typing import Iterator
from typing import Generator

T1 = TypeVar("T1")


def drop_none(iterator: Iterator[T1]) -> Generator[T1, None, None]:
    for i in iterator:
        if i is not None:
            yield i

def some(arg: Any) -> bool:
    return arg is not None