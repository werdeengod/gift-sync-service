import asyncio
from dishka import FromDishka

from src.adapters.workers.args import ArgsParser
from src.bootstrap import build_container
from src.application.use_cases import SyncGiftsUseCase
from src.infrastructure.worker import Worker, WorkerRunner

args = ArgsParser().get_args()
worker = Worker(build_container())


@worker.task(
    workers=args.workers,
    max_retries=args.retries,
    retry_delay=args.delay,
    timeout=args.timeout,
)
async def sync_telegram_gifts(sync_gifts: FromDishka[SyncGiftsUseCase]):
    await sync_gifts.execute()


async def main():
    runner = WorkerRunner(worker)
    await runner.run()

if __name__ == '__main__':
    asyncio.run(main())
