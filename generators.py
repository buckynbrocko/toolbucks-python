from typing import Any
from typing import Generator


def consume(generator: Generator[Any, None, None]) -> None:
    for _ in generator:
        ...
