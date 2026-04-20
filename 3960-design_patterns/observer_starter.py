#!/usr/bin/env python3
from __future__ import annotations
from typing import Protocol


class Observer(Protocol):
    def update(self, topic: str, data: str) -> None: ...


class NewsSubject:
    def __init__(self) -> None:
        self._subs: dict[Observer, set[str] | None] = {}

    def subscribe(self, observer: Observer, topics: set[str] | None = None) -> None:
        if observer in self._subs:
            return  # ignore duplicate subscribe for same instance
        self._subs[observer] = topics

    def unsubscribe(self, observer: Observer) -> None:
        self._subs.pop(observer, None)

    def notify(self, topic: str, data: str) -> None:
        for observer, interests in list(self._subs.items()):
            if interests is not None and topic not in interests:
                continue
            observer.update(topic, data)


class LogObserver:
    def update(self, topic: str, data: str) -> None:
        print(f"log:{topic}={data}")


class EmailObserver:
    def update(self, topic: str, data: str) -> None:
        print(f"email:{topic}={data}")


# TODO: implement SmsObserver
# Its update(topic, data) method must print:  sms:<topic>=<data>


def main() -> None:
    subject = NewsSubject()

    log = LogObserver()
    email = EmailObserver()

    subject.subscribe(log, topics={"sports", "breaking"})
    subject.subscribe(email)  # None = receives all topics

    # TODO: instantiate SmsObserver and subscribe it to topics={"breaking"} only

    subject.notify("weather", "rain")
    subject.notify("sports", "goal")
    subject.notify("breaking", "alert")


if __name__ == "__main__":
    main()
