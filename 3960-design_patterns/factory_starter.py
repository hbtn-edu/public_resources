#!/usr/bin/env python3
from __future__ import annotations


class Bus:
    def mode(self) -> str:
        return "road"


class Train:
    def mode(self) -> str:
        return "rails"


class Bike:
    def mode(self) -> str:
        return "lane"


class Scooter:
    def mode(self) -> str:
        return "scooter_lane"


class VehicleFactory:
    def __init__(self) -> None:
        self._registry: dict[str, type] = {
            "bus": Bus,
            "train": Train,
            "bike": Bike,
        }

    def register_kind(self, name: str, cls: type) -> None:
        self._registry[name] = cls

    def create(self, kind: str) -> object:
        if kind not in self._registry:
            raise ValueError(f"Unknown vehicle kind: {kind!r}")
        return self._registry[kind]()


def main() -> None:
    factory = VehicleFactory()

    print(factory.create("bus").mode())
    print(factory.create("train").mode())
    print(factory.create("bike").mode())

    # TODO: register Scooter with factory.register_kind(...)
    # TODO: print factory.create("scooter").mode()


if __name__ == "__main__":
    main()
