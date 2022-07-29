import random
import time

from aiohttp import web

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


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
