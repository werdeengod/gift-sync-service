# Gift Sync Service

Сервис синхронизации подарков из Telegram с отправкой событий через Outbox + Kafka.

## 📋 Описание

Сервис предназначен для:
- Синхронизации подарков из Telegram (MTProto) API
- Хранения данных в PostgreSQL
- Отправки идемпотентных событий об изменениях в RabbitMQ через паттерн Outbox
- Обработки фоновых задач через самописный воркер с retry (экспоненциальная задержка с джиттером), таймаутами, fallback, DI-интеграцией, горизонтальным масштабированием и graceful shutdown

## 🏗 Архитектура

Проект построен на **гексагональной архитектуре** (Hexagonal/Ports & Adapters):

| Слой | Назначение | Содержит                                                               |
| :--- | :--- |:-----------------------------------------------------------------------|
| **Domain** | Бизнес-логика | Entities, Exceptions, Value Objects, Domain Events, Ports (интерфейсы) |
| **Application** | Сценарии использования | Use Cases, DTO                                                         |
| **Adapters** | Входящие адаптеры | REST API, Workers                                                      |
| **Infrastructure** | Исходящие адаптеры | PostgreSQL, RabbitMQ, Telegram API, Worker Engine                      |
