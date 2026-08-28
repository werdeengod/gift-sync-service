from dishka import make_async_container
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
        DatabaseProvider(),
        RepositoryProvider(),
        TelegramProvider(),
        EventProvider(),
        SerializerProvider(),
        MapperProvider(),
        UseCaseProvider()
    )
