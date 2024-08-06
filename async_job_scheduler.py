import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from cron_jobs.round_end import round_end_logic
from cron_jobs.cleanup_images import cleanup_unused_images
from redis_logic import job_lock_wrapper


async def print_something():
    await asyncio.sleep(1)
    print("Hey")


ascheduler = AsyncIOScheduler()
ascheduler.add_job(round_end_logic, CronTrigger(day_of_week="mon", hour=0, minute=30))
ascheduler.add_job(
    job_lock_wrapper("some_key", print_something), IntervalTrigger(seconds=10)
)
ascheduler.add_job(
    cleanup_unused_images, CronTrigger(day_of_week="mon", hour=0, minute=45)
)
