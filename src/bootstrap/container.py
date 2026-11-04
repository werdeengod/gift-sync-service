from dishka import make_async_container

from src.config import config
from src.bootstrap.providers import (
    DatabaseProvider,
    RepositoryProvider,
    TelegramProvider,
    EventProvider,
    SerializerProvider,
    MapperProvider,
    UseCaseProvider
)


def build_container():
    return make_async_container(
        DatabaseProvider(config.db_url),
        RepositoryProvider(),
        TelegramProvider(),
        EventProvider(config.broker_url),
        SerializerProvider(),
        MapperProvider(),
        UseCaseProvider()
    )
