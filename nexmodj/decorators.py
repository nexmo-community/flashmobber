from enum import Enum
from datetime import datetime
from functools import wraps
import json

from django.http import HttpResponse

import attr
from marshmallow import Schema, fields, post_load

from .models import SMSMessagePart

from . import client


@attr.s
class IncomingSMS:
    message_id = attr.ib(type=str)
    msisdn = attr.ib(type=str)
    to = attr.ib(type=str)
    type = attr.ib(
        type=str,
        validator=attr.validators.in_(['text', 'unicode', 'binary']))
    message_timestamp = attr.ib(type=datetime)
    timestamp = attr.ib(type=datetime)

    keyword = attr.ib(type=str, default=None)
    text = attr.ib(type=str, default=None)
    # TODO: Need to do something with these:
    data = attr.ib(default=None)
    udh = attr.ib(default=None)

    concat = attr.ib(type=bool, default=False)
    concat_part = attr.ib(type=int, default=None)
    concat_ref = attr.ib(type=str, default=None)
    concat_total = attr.ib(type=int, default=None)


class Timestamp(fields.Field):
    def _deserialize(self, value, attr, data):
        return datetime.fromtimestamp(int(value))


class IncomingSMSSchema(Schema):
    msisdn = fields.Str()
    to = fields.Str()
    message_id = fields.Str(data_key='messageId')
    text = fields.Str()
    type = fields.Str(data_key='type')
    keyword = fields.Str()
    message_timestamp = fields.DateTime(data_key='message-timestamp', format='%Y-%m-%d %H:%M:%S')
    timestamp = Timestamp()

    concat = fields.Bool()
    concat_part = fields.Int(data_key='concat-part')
    concat_ref = fields.Str(data_key='concat-ref')
    concat_total = fields.Int(data_key='concat-total')

    # TODO: Need to do something with these:
    data = fields.Str()
    udh = fields.Str()

    @post_load
    def make_sms(self, data):
        print(data)
        return IncomingSMS(**data)


def sms_webhook(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        try:
            if request.method != 'POST':
                return HttpResponse("Method not allowed: {}".format(request.method), status=405)
            if request.content_type != 'application/json':
                return HttpResponse("Unsupported request content-type.", status=415)
            data = json.loads(request.body.decode('utf-8'))
            if client.check_signature(data):
                if data.get('concat') == 'true':
                    # Put it in the database.
                    # Then query if we have all the parts
                    # and run func if necessary.
                    pass
                else:
                    return func(request, *args, *kwargs)
            return HttpResponse("Invalid signature.", status=403, reason="Invalid signature.")
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON payload provided.", status=400)
    return inner