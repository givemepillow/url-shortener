import typing as tp

from aiohttp import web
from sqlalchemy import select

from aiohttp_apispec import docs

from url_shortner.api.utils import cache
from url_shortner.db.base import Session
from url_shortner.db.model import urls


class ShortURLView(web.View):
    URL_PATH = "/api/v1/{short_url}"
    session = Session

    @docs(tags=['short-url'], responses={
        301: {"description": "Redirect to origin URL."},
        404: {"description": "Origin URL not found."},
        500: {"description": "Server error"},
    }, )
    async def get(self):
        short_url: str = self.request.match_info.get("short_url")
        long_url = await self.get_long_url(short_url)
        if long_url:
            return web.HTTPFound(long_url)
        raise web.HTTPNotFound(text='Origin URL not found.')

    @cache
    async def get_long_url(self, short_url: str) -> tp.Optional[str]:
        async with self.session() as s:
            return (await s.execute(select(urls.c.long_url).where(urls.c.short_url == short_url))).scalar()
