from celery import Celery

from app.adapter.persistence import redis_connect
from app.config import load_config


def create_app() -> Celery:
    config = load_config()
    redis_url = config.redis.url
    app = Celery(__name__)
    app.conf.broker_url = redis_url
    app.conf.result_backend = redis_url
    return app


redis = redis_connect(load_config().redis.url)
app_redis = create_app()
