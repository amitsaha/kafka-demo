from consumer.consumer import consume_metrics
import json
from collections import namedtuple

ConsumerRecord = namedtuple("ConsumerRecord", ["value"])


def FakeConsumer():
    d = json.dumps(
        {
            "node_id": "node123",
            "cpu_usage_percent": 89.9,
            "memory_usage_percent": 26.1,
            "timestamp": 121211,
        }
    )
    msgs = [d, d, d, d, d]

    for record in msgs:
        yield ConsumerRecord(record)


class FakeCursor:
    def __init__(self):
        pass

    def execute(self, sql, d):
        pass

    def close(self):
        pass


class FakeDB:
    def __init__(self):
        self.c = None
        self.cursor_execute = 0

    def cursor(self):
        self.cursor_execute += 1
        self.c = FakeCursor()
        return self.c

    def commit(self):
        pass


def test_consume_metrics():

    c = FakeConsumer()
    db = FakeDB()
    consume_metrics(c, db)

    # assert store_db() was called five times
    # one for each of the metric values
    assert db.cursor_execute == 5
