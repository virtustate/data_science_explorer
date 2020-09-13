from django.db import models
import datetime

CONNECTION_TYPE_CHOICES = (
    ('csv', 'csv'),
    ('Snowflake', 'Snowflake'),
)

def filer_on_delete():
    print('filter_on_delete')
    
class Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, default='', max_length=50)
    connection_type = models.CharField(choices=CONNECTION_TYPE_CHOICES, default='csv', max_length=20)
    created = models.DateTimeField(null=True)
