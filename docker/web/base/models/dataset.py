from django.db import models
import datetime
from filer.fields.file import FilerFileField
import pandas
from base.redis_db import RedisDB

CONNECTION_TYPE_CHOICES = (
    ('local text', 'local text'),
    ('Snowflake', 'Snowflake'),
)
DELIMTER_CHOICES = ((',', 'comma'), ('\t', 'tab'), ('\s+', 'space'))

def filer_on_delete():
    print('filter_on_delete')
    
class Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, default='', max_length=50)
    connection_type = models.CharField(choices=CONNECTION_TYPE_CHOICES, default='csv', max_length=20)
    created = models.DateTimeField(null=True)
    file = FilerFileField
    delimiter = models.CharField(choices=DELIMTER_CHOICES, max_length=10, default=',')
    header = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def load_file_to_redis(self, filename):
        header = 0 if self.header else None
        df=pandas.read_csv(filename, header=header, sep=self.delimiter)
        my_redis = RedisDB(self.id)
        my_redis.start_load()
        my_redis.set('dataframe', df.to_csv())
        my_redis.end_load()

    


