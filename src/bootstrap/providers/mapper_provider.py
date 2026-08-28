from dishka import Provider, Scope, provide

from src.infrastructure.database.mappers import GiftMapper, OutboxMapper


class MapperProvider(Provider):
    @provide(scope=Scope.APP)
    def get_database_gift_mapper(self) -> GiftMapper:
        return GiftMapper()

    @provide(scope=Scope.APP)
    def get_database_gift_mapper(self) -> OutboxMapper:
        return OutboxMapper()


