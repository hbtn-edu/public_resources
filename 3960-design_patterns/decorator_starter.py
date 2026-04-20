#!/usr/bin/env python3
from __future__ import annotations
from abc import ABC, abstractmethod


class Beverage(ABC):
    @abstractmethod
    def cost(self) -> int: ...

    @abstractmethod
    def description(self) -> str: ...


class Coffee(Beverage):
    def cost(self) -> int:
        return 50

    def description(self) -> str:
        return "Coffee"


class MilkDecorator(Beverage):
    def __init__(self, inner: Beverage) -> None:
        self._inner = inner

    def cost(self) -> int:
        return self._inner.cost() + 10

    def description(self) -> str:
        return self._inner.description() + " + milk"


class SugarDecorator(Beverage):
    def __init__(self, inner: Beverage) -> None:
        self._inner = inner

    def cost(self) -> int:
        return self._inner.cost() + 5

    def description(self) -> str:
        return self._inner.description() + " + sugar"


# TODO: implement CaramelDecorator following the same pattern as MilkDecorator
# cost(): self._inner.cost() + 15
# description(): self._inner.description() + " + caramel"


def main() -> None:
    cup1 = MilkDecorator(Coffee())
    print(cup1.description(), cup1.cost())

    cup2 = MilkDecorator(SugarDecorator(Coffee()))
    print(cup2.description(), cup2.cost())

    # TODO: build CaramelDecorator(MilkDecorator(SugarDecorator(Coffee()))) and print it


if __name__ == "__main__":
    main()
