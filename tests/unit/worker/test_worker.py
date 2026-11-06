import pytest
from unittest.mock import AsyncMock

from dishka import Scope, FromDishka
from src.infrastructure.worker import Context


class TestWorker:
    @pytest.mark.asyncio
    async def test_inject_dependencies(self, worker, container):
        @worker.task(name="test_task")
        async def test_handler(ctx: Context, service: FromDishka[AsyncMock]):
            return await service.get_data()

        request_scope = container(Scope.REQUEST)
        context = Context()

        dependencies = await worker._inject_dependencies(
            handler=test_handler,
            ctx=context,
            request_scope=request_scope
        )

        assert "ctx" in dependencies
        assert "service" in dependencies
        assert isinstance(dependencies["service"], AsyncMock)

    @pytest.mark.asyncio
    async def test_retry_on_failure(self, worker):
        mock_handler = AsyncMock()
        mock_handler.side_effect = [
            Exception("Error 1"),
            Exception("Error 2"),
            {"success": True}
        ]

        @worker.task(name="test_task", max_retries=3, retry_delay=0.01)
        async def test_handler():
            return await mock_handler()

        context = Context()
        request_scope = AsyncMock()
        worker._is_running = True

        result = await worker._execute_with_retry(
            task=worker.tasks["test_task"],
            context=context,
            request_scope=request_scope
        )

        assert mock_handler.call_count == 3
        assert result == {"success": True}
        assert len(context.errors) == 2

    @pytest.mark.asyncio
    async def test_fallback_called_after_retries(self, worker):
        mock_handler = AsyncMock()
        mock_handler.side_effect = Exception("Permanent error")

        async def mock_fallback():
            return {"fallback": "done"}

        @worker.task(
            name="test_task",
            max_retries=2,
            retry_delay=0.01,
            fallback=mock_fallback
        )
        async def test_handler():
            return await mock_handler()

        context = Context()
        request_scope = AsyncMock()
        worker._is_running = True

        result = await worker._execute_with_retry(
            task=worker.tasks["test_task"],
            context=context,
            request_scope=request_scope
        )

        assert mock_handler.call_count == 2
        assert result == {"fallback": "done"}
