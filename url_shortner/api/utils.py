import random
import time
import typing as tp

from aiohttp import web

from url_shortner.db.base import redis

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
EXPIRE = 3600 * 60 * 6  # seconds


def json_response(
        status: int = 200, text_status: str = "ok", data: dict = None
) -> web.Response:
    return web.json_response(status=status, data={"data": data, "status": text_status})


def error_json_response(
        status: int = 400,
        text_status: str = "ok",
        message: str = "Bad request",
        data: dict = None,
) -> web.Response:
    return web.json_response(
        status=status, data={"data": data, "status": text_status, "message": message}
    )


def base62_encode(number: int) -> str:
    if number == 0:
        return BASE62[0]
    arr = []
    base = len(BASE62)
    while number:
        number, rem = divmod(number, base)
        arr.append(BASE62[rem])
    arr.reverse()
    return ''.join(arr)


def unique_id_generator():
    i = random.randint(0, 100)
    while True:
        i %= 1000
        yield int(round(time.time() * 1000)) + i
        i += 1


def cache(func: tp.Callable):
    async def wrapper(self, short_url: str):
        long_url = (await redis.get(short_url))
        if long_url:
            return long_url.decode("utf-8")
        long_url = await func(self, short_url)
        await redis.set(name=short_url, value=long_url, ex=EXPIRE)
        return long_url

    return wrapper
