
from datetime import datetime, timezone
import json
from pprint import pprint

import nexmodj as n
import nexmodj.decorators as d
import nexmodj.models as models

from unittest.mock import MagicMock

import pytest


def test_parse_part():
    part_data = json.loads('''{
    "concat": "true",
    "concat-part": "1",
    "concat-ref": "78",
    "concat-total": "9",
    "keyword": "LOREM",
    "message-timestamp": "2018-04-24 14:05:19",
    "messageId": "0B000000D0EBB58D",
    "msisdn": "447700900419",
    "nonce": "0a455d75-459e-446c-9072-698728516d7c",
    "sig": "c4bc6301949691b6093772ba246a35eb",
    "text": "Lorem Ipsum is simply dummy text of the printing and typesetting in",
    "timestamp": "1524578719",
    "to": "447700900996",
    "type": "unicode"
}''')
    sms = d.IncomingSMSSchema().load(part_data)
    assert isinstance(sms, d.IncomingSMS)
    assert sms.concat == True
    assert sms.concat_part == 1
    assert sms.concat_total == 9
    assert sms.concat_ref == "78"
    assert sms.keyword == "LOREM"
    assert sms.message_timestamp == datetime(2018, 4, 24, 14, 5, 19, tzinfo=timezone.utc)
    assert sms.message_id == '0B000000D0EBB58D'
    assert sms.msisdn == '447700900419'
    assert sms.to == '447700900996'
    assert sms.text == 'Lorem Ipsum is simply dummy text of the printing and typesetting in'
    assert sms.timestamp == datetime(2018, 4, 24, 14, 5, 19, tzinfo=timezone.utc)
    assert sms.type == 'unicode'


def test_to_model():
    part_data = json.loads('''{
    "concat": "true",
    "concat-part": "1",
    "concat-ref": "78",
    "concat-total": "9",
    "keyword": "LOREM",
    "message-timestamp": "2018-04-24 14:05:19",
    "messageId": "0B000000D0EBB58D",
    "msisdn": "447700900419",
    "nonce": "0a455d75-459e-446c-9072-698728516d7c",
    "sig": "c4bc6301949691b6093772ba246a35eb",
    "text": "Lorem Ipsum is simply dummy text of the printing and typesetting in",
    "timestamp": "1524578719",
    "to": "447700900996",
    "type": "unicode"
}
''')
    sms = d.IncomingSMSSchema().load(part_data).to_model()
    assert isinstance(sms, models.SMSMessagePart)
    assert not hasattr(sms, 'concat')   # Just make sure we're looking at the model.
    assert sms.concat_part == 1
    assert sms.concat_total == 9
    assert sms.concat_ref == "78"
    assert sms.keyword == "LOREM"
    assert sms.message_timestamp == datetime(2018, 4, 24, 14, 5, 19, tzinfo=timezone.utc)
    assert sms.message_id == '0B000000D0EBB58D'
    assert sms.msisdn == '447700900419'
    assert sms.to == '447700900996'
    assert sms.text == 'Lorem Ipsum is simply dummy text of the printing and typesetting in'
    assert sms.timestamp == datetime(2018, 4, 24, 14, 5, 19, tzinfo=timezone.utc)
    assert sms.type == 'unicode'


@pytest.mark.django_db
def test_decorator(rf):
    js = '''{
    "concat": "true",
    "concat-part": "1",
    "concat-ref": "78",
    "concat-total": "9",
    "keyword": "LOREM",
    "message-timestamp": "2018-04-24 14:05:19",
    "messageId": "0B000000D0EBB58D",
    "msisdn": "447700900419",
    "nonce": "0a455d75-459e-446c-9072-698728516d7c",
    "sig": "c4bc6301949691b6093772ba246a35eb",
    "text": "Lorem Ipsum is simply dummy text of the printing and typesetting in",
    "timestamp": "1524578719",
    "to": "447700900996",
    "type": "unicode"
}'''
    request = rf.post('/sms/incoming', content_type='application/json', data=js)
    view = MagicMock()
    decorated = d.sms_webhook(view)

    response = decorated(request)

    assert response.status_code == 200
    assert models.SMSMessagePart.objects.get(concat_ref='78') is not None