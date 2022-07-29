from marshmallow import Schema, fields


class LongURLSchema(Schema):
    long_url = fields.Url(required=True, relative=False, require_tld=False, data_key="longURL")


class ShortURLSchema(Schema):
    short_url = fields.Url(required=True, relative=False, require_tld=False, data_key="shortURL")
