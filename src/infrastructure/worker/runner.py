from typing import TYPE_CHECKING
import signal
import logging
import asyncio


if TYPE_CHECKING:
    from .worker import Worker


logger = logging.getLogger(__name__)


class WorkerRunner:
    def __init__(self, worker: 'Worker'):
        self.worker = worker
        self._stop_event = asyncio.Event()

    def _signal_handler(self):
        logger.info("Received stop signal")
        self._stop_event.set()

    async def run(self, timeout: float = 10.0):
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self._signal_handler)
            except NotImplementedError:
                pass

        worker_task = asyncio.create_task(self.worker.start())
        logger.info("Worker started. Press Ctrl+C to stop.")

        try:
            await self._stop_event.wait()
        finally:
            await self.worker.stop(timeout=timeout)
            if not worker_task.done():
                await worker_task
