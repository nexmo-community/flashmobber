from django.db import models


class SMSMessagePart(models.Model):
    concat_ref = models.CharField(max_length=32, db_index=True)

    message_id = models.CharField(max_length=32)
    msisdn = models.CharField(max_length=24)
    to = models.CharField(max_length=24)

    text = models.CharField(max_length=160)
    # TODO: Need to do something with these:
    data = models.BinaryField(max_length=160)
    udh = models.BinaryField(max_length=160)

    type = models.CharField(
        max_length=7, choices=[('text', 'Text'), ('unicode', 'Unicode'), ('binary', 'Binary')])
    keyword = models.CharField(max_length=160)
    message_timestamp = models.DateTimeField()
    timestamp = models.DateTimeField()

    concat_part = models.IntegerField()
    concat_ref = models.CharField(max_length=32)
    concat_total = models.IntegerField()