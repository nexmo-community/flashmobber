# Generated by Django 2.0.4 on 2018-04-26 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMSMessagePart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.CharField(max_length=32)),
                ('msisdn', models.CharField(max_length=24)),
                ('to', models.CharField(max_length=24)),
                ('text', models.CharField(max_length=160)),
                ('data', models.BinaryField(max_length=160)),
                ('udh', models.BinaryField(max_length=160)),
                ('type', models.CharField(choices=[('text', 'Text'), ('unicode', 'Unicode'), ('binary', 'Binary')], max_length=7)),
                ('keyword', models.CharField(max_length=160)),
                ('message_timestamp', models.DateTimeField()),
                ('timestamp', models.DateTimeField()),
                ('concat_part', models.IntegerField()),
                ('concat_ref', models.CharField(max_length=32)),
                ('concat_total', models.IntegerField()),
            ],
        ),
    ]
