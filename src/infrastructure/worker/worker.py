from typing import Optional, Callable, get_type_hints
import asyncio
import logging

from dishka import AsyncContainer, Scope
from .entites import Task
from .context import Context


logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, container: 'AsyncContainer', *, delay: int = 10):
        self._container = container
        self._delay = delay

        self.tasks: dict[str, Task] = {}
        self.workers = []

        self._is_running = False
        self._stop_event = asyncio.Event()

    def task(
            self,
            name: Optional[str] = None,
            workers: int = 1,
            max_retries: int = 3,
            retry_delay: float = 1.0,
            timeout: Optional[float] = None,
            fallback: Optional[Callable] = None
    ):
        """
            Декоратор для регистрации задачи

            Использование:
                @worker.task()
                async def my_task():
                    ...

                @worker.task(name="custom_name", max_retries=5)
                async def another_task():
                    ...
        """
        def decorator(handler: Callable):
            task_name = name or handler.__name__

            self.tasks[task_name] = Task(
                name=task_name,
                handler=handler,
                max_retries=max_retries,
                retry_delay=retry_delay,
                timeout=timeout,
                fallback=fallback,
                workers=workers
            )

            return handler

        return decorator

    @staticmethod
    async def _inject_dependencies(
            ctx: Context,
            handler: Callable,
            request_scope: 'AsyncContainer',
            dependencies: Optional[dict] = None
    ) -> dict:
        if not dependencies:
            dependencies = {}

        type_hints = get_type_hints(handler)

        for param_name, param_type in type_hints.items():
            if param_name in dependencies:
                continue

            if param_type == Context:
                dependencies[param_name] = ctx
                continue

            dep = await request_scope.get(param_type)
            dependencies[param_name] = dep

        return dependencies

    async def _execute_fallback(self, task: 'Task', context: 'Context', request_scope: 'AsyncContainer', attempt: int):
        logger.info(f"Executing fallback for task '{task.name}' after {attempt} attempts")
        logger.debug(f"Fallback errors: {[str(e) for e in context.errors]}")

        try:
            dependencies = await self._inject_dependencies(
                handler=task.fallback,
                ctx=context,
                request_scope=request_scope
            )

            if task.timeout:
                result = await asyncio.wait_for(
                    task.fallback(**dependencies),
                    timeout=task.timeout
                )
            else:
                result = await task.fallback(**dependencies)

            logger.info(f"Fallback for task '{task.name}' completed successfully")
            await asyncio.sleep(0.2)
            return result

        except asyncio.CancelledError:
            logger.debug(f"Fallback for task '{task.name}' cancelled")
            raise

        except asyncio.TimeoutError:
            logger.error(f"Fallback for task '{task.name}' timed out after {task.timeout}s")
            raise RuntimeError(
                f"Task '{task.name}' failed after {attempt} attempts and fallback timed out"
            ) from context.get_last_error()

    async def _execute_with_retry(self, task: 'Task', context: 'Context', request_scope: 'AsyncContainer'):
        attempt = 0

        while self._is_running and not self._stop_event.is_set():
            try:
                attempt += 1
                logger.debug(f"Executing task '{task.name}' (attempt {attempt})")

                dependencies = await self._inject_dependencies(
                    handler=task.handler,
                    ctx=context,
                    request_scope=request_scope
                )

                if task.timeout:
                    result = await asyncio.wait_for(
                        task.handler(**dependencies),
                        timeout=task.timeout
                    )
                else:
                    result = await task.handler(**dependencies)

                attempt = 0
                await asyncio.sleep(0.2)
                return result

            except asyncio.CancelledError:
                logger.debug(f"Task '{task.name}' cancelled during execution")
                raise

            except Exception as e:
                context.add_error(e)
                logger.error(f"Task '{task.name}' failed (attempt {attempt}): {e}")

                if attempt >= task.max_retries:
                    logger.error(f"Task '{task.name}' max retries exceeded")
                    break

                await asyncio.sleep(task.get_delay(attempt))

        if not task.fallback:
            last_error = context.get_last_error()
            raise RuntimeError(
                f"Task '{task.name}' failed after {task.max_retries} retries"
            ) from last_error

        return await self._execute_fallback(
            task=task,
            context=context,
            attempt=attempt,
            request_scope=request_scope
        )

    async def _send_task(self, task: 'Task', worker_id: int):
        logger.info(f"Starting worker {worker_id} for task '{task.name}'")

        while self._is_running and not self._stop_event.is_set():
            request_scope = self._container(Scope.REQUEST)
            context = Context()

            try:
                await self._execute_with_retry(
                    task=task,
                    context=context,
                    request_scope=request_scope
                )

            except asyncio.CancelledError:
                logger.info(f"Worker {worker_id} for task '{task.name}' cancelled")
                break

            except Exception as e:
                logger.error(f"Worker {worker_id} for task '{task.name}' failed: {e}")

            finally:
                await request_scope.close()

            await asyncio.sleep(self._delay)

    async def start(self):
        if self._is_running:
            logger.warning("Worker already running")
            return

        logger.info(f"Worker is running")
        self._is_running = True
        self._stop_event.clear()

        self.workers = [
            asyncio.create_task(self._send_task(task, worker_id=worker_id))
            for task in self.tasks.values()
            for worker_id in range(task.workers)
        ]

        await asyncio.gather(*self.workers, return_exceptions=True)

    async def stop(self, timeout: float = 10.0):
        if not self._is_running:
            logger.warning("Worker not running")
            return

        logger.info(f"Worker is stopped")
        self._is_running = False
        self._stop_event.set()

        for handle in self.workers:
            if not handle.done():
                handle.cancel()

        try:
            await asyncio.wait_for(
                asyncio.gather(*self.workers, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.warning("Some workers didn't stop in time")

        self.workers.clear()
        await self._container.close()

