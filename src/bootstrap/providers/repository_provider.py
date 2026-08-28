from dishka import Provider, Scope, provide, FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.repositories import GiftRepository, OutboxRepository
from src.infrastructure.database.mappers import GiftMapper, OutboxMapper
from src.infrastructure.serializers import EventSerializer, GiftSerializer
from src.domain.ports.database.repositories import GiftRepositoryPort, OutboxRepositoryPort


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=GiftRepositoryPort)
    def get_gift_repo(
            self,
            session: FromDishka[AsyncSession],
            mapper: FromDishka[GiftMapper],
            serializer: FromDishka[GiftSerializer],
    ) -> GiftRepository:
        return GiftRepository(
            session=session,
            gift_mapper=mapper,
            gift_serializer=serializer
        )

    @provide(scope=Scope.REQUEST, provides=OutboxRepositoryPort)
    def get_outbox_repo(
            self,
            session: FromDishka[AsyncSession],
            mapper: FromDishka[OutboxMapper],
            serializer: FromDishka[EventSerializer],
    ) -> OutboxRepository:
        return OutboxRepository(
            session=session,
            outbox_mapper=mapper,
            event_serializer=serializer
        )