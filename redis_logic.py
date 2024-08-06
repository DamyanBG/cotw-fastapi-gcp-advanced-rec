from contextlib import asynccontextmanager

from redis.asyncio import Redis

redis_client = Redis(host="localhost", port=6379, db=0)


@asynccontextmanager
async def acquire_lock(lock_key, expiration=30):
    lock = redis_client.lock(lock_key, timeout=expiration)
    acquired = await lock.acquire(blocking=False)
    try:
        if acquired:
            yield
        else:
            raise Exception("The lock is already acquired!")
    finally:
        await lock.release()


def job_lock_wrapper(lock_key, func, expiration=30):
    async def job_with_lock():
        try:
            async with acquire_lock(lock_key, expiration):
                await func()
        except Exception:
            pass

    return job_with_lock
    