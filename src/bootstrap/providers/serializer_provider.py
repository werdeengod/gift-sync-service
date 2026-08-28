from dishka import Provider, Scope, provide, FromDishka

from src.domain.entities import Gift, OutboxMessage
from src.domain.events import DomainEvent
from src.infrastructure.serializers import GiftSerializer, EventSerializer, JsonSerializer, OutboxMessageSerializer


class SerializerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_gift_serializer(self) -> GiftSerializer:
        return GiftSerializer()

    @provide(scope=Scope.APP)
    def get_outbox_serializer(self) -> OutboxMessageSerializer:
        return OutboxMessageSerializer()

    @provide(scope=Scope.APP)
    def get_event_serializer(
            self,
            gift_serializer: FromDishka[GiftSerializer],
    ) -> EventSerializer:
        return EventSerializer(gift_serializer)

    @provide(scope=Scope.APP, provides=JsonSerializer[Gift])
    def get_gift_json_serializer(
            self,
            base: FromDishka[GiftSerializer],
    ) -> JsonSerializer[Gift]:
        return JsonSerializer(base)

    @provide(scope=Scope.APP, provides=JsonSerializer[DomainEvent])
    def get_event_json_serializer(
            self,
            base: FromDishka[EventSerializer],
    ) -> JsonSerializer[DomainEvent]:
        return JsonSerializer(base)

    @provide(scope=Scope.APP, provides=JsonSerializer[OutboxMessage])
    def get_outbox_json_serializer(
            self,
            base: FromDishka[OutboxMessageSerializer],
    ) -> JsonSerializer[OutboxMessage]:
        return JsonSerializer(base)


