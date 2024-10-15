from faststream.kafka import KafkaBroker

from app.config import KafkaConfig


def new_broker(config: KafkaConfig) -> KafkaBroker:
    return KafkaBroker(
        config.url,
    )
