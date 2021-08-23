from django.db import models
import datetime

from django.db.models.fields import CharField
from base.models.dataset import Dataset
from django.contrib.postgres.fields import ArrayField


class Analysis(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, default='', max_length=50)
    created = models.DateTimeField(null=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='AnalysisDataset')
    dependent_column = models.CharField(null=False, default='', max_length=100) 
    datetime_column = models.CharField(null=False, default='', max_length=100)
    independent_columns = ArrayField(CharField(max_length=100))

    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name