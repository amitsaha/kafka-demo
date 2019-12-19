from producer.metrics import publish_metrics


class FakeKafkaProducer:
    """A FakeKafkaProducer """

    def __init__(self):
        self.num_send = 0

    def send(self, topic, data):
        # Check default topic name
        assert topic == "metrics"

        # Keep a counter of messages published to assert it in test
        self.num_send += 1

        # Validate the fields being attempted to be published
        expected_fields = [
            "node_id",
            "cpu_usage_percent",
            "memory_usage_percent",
            "timestamp",
        ]
        for f in expected_fields:
            assert f in data.keys()


def test_publish_metrics():
    """ Test that the send() method is called for every publish_metrics() call """
    p = FakeKafkaProducer()
    publish_metrics(p)
    publish_metrics(p)
    assert p.num_send == 2
