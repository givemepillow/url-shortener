import os

from aiohttp import web

from aiohttp_apispec import response_schema, request_schema, docs
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from url_shortner.db.model import urls
from url_shortner.api.schemas import LongURLSchema, ShortURLSchema
from url_shortner.db.base import Session
from url_shortner.api.utils import base62_encode, unique_id_generator, json_response


class LongURLView(web.View):
    URL_PATH = "/api/v1/url/shorten"
    ID_GENERATOR = unique_id_generator()
    session = Session

    @docs(tags=['long-url'], responses={
        201: {"description": "Ok. Short URL created.", "schema": ShortURLSchema},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    }, )
    @request_schema(LongURLSchema())
    @response_schema(ShortURLSchema(), 201)
    async def post(self):
        long_url = self.clear_url(self.request['data'].get('long_url'))
        short_path = await self.create_short_url(long_url)
        return json_response(
            status=201,
            text_status='Short URL hase benn created!',
            data=ShortURLSchema().dump({"short_url": f"{os.environ['HOST']}/api/v1/{short_path}"})
        )

    def unique_id(self) -> int:
        return next(self.ID_GENERATOR)

    async def create_short_url(self, long_url: str) -> str:
        async with self.session() as s:
            async with s.begin():
                _short_url = (await s.execute(
                    select(urls.c.short_url).
                    where(urls.c.long_url == long_url)
                )).scalar()
                if _short_url:
                    return _short_url
                _short_url = base62_encode(self.unique_id())
                _short_url = (await s.execute(
                    insert(urls).
                    values(long_url=long_url, short_url=_short_url).
                    returning(urls.c.short_url)
                )).scalar()
                return _short_url

    @staticmethod
    def clear_url(long_url):
        if long_url[-1] == '/':
            return long_url[:-1]
        return long_url
