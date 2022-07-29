import os

from aiohttp import web

from aiohttp_apispec import response_schema, request_schema, docs
from sqlalchemy.dialects.postgresql import insert

from url_shortner.db.model import urls
from url_shortner.api.schemas import LongURLSchema, ShortURLSchema
from url_shortner.db.session import Session
from url_shortner.api.utils import base62_encode, unique_id_generator, json_response


class LongURLView(web.View):
    URL_PATH = "/api/v1/url/shorten"
    OFFSET = 1000
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
        long_url = self.request['data'].get('long_url')
        short_path = self.create_short_url(self.unique_id())
        await self.save_url(long_url=long_url, short_url=short_path)
        return json_response(
            status=201,
            text_status='Short URL hase benn created!',
            data=ShortURLSchema().dump({"short_url": f"{os.environ['HOST']}/api/v1/{short_path}"})
        )

    def create_short_url(self, unique_id: int):
        return base62_encode(unique_id + self.OFFSET)

    def unique_id(self) -> int:
        return next(self.ID_GENERATOR)

    async def save_url(self, long_url: str, short_url: str) -> None:
        async with self.session() as s:
            async with s.begin():
                await s.execute(insert(urls).values(long_url=long_url, short_url=short_url))
