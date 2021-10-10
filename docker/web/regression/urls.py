from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'Regression'

urlpatterns = [
    path('', RegressionListView.as_view(), name='regression_list',),
    path('create', RegressionCreateView.as_view(), name='regression_create'),
    path('delete/<int:pk>', RegressionDeleteView.as_view(), name='regression_delete'),
    path('view/<int:pk>', RegressionViewView.as_view(), name='regression_view'),
]
