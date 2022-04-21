from django.db import models
import datetime
from base.models.ResultMixin import ResultMixin

from django.db.models.fields import CharField
from base.models.dataset import Dataset
from django.contrib.postgres.fields import ArrayField


class Analysis(ResultMixin, models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=50)
    created = models.DateTimeField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='AnalysisDataset')
    dependent_column = models.CharField(null=True, max_length=100) 
    datetime_column = models.CharField(null=True, max_length=100)
    independent_columns = ArrayField(CharField(null=True, max_length=100), null=True)

    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name