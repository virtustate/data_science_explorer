from django.db import models
from base.models.analysis import Analysis



class Regression(Analysis):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='AnalysisDataset')
    dependent_column = models.CharField(null=False, default='', max_length=100) 