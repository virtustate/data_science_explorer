from django.db import models
import datetime

CONNECTION_TYPE_CHOICES = (
    ('csv', 'csv'),
    ('Snowflake', 'Snowflake'),
)

class Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, default='', max_length=50)
    connection_type = models.CharField(choices=CONNECTION_TYPE_CHOICES, default='csv', max_length=20)
    redis_db = models.IntegerField(null=True)
    last_loaded = models.DateTimeField(null=True)