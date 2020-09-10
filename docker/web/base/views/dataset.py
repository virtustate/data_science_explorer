from django.views.generic import View
from django.shortcuts import render,redirect
from django.conf import settings
from base.models.dataset import Dataset,CONNECTION_TYPE_CHOICES
from django import forms
import base.helpers as helpers
from base.redis_db import RedisDB
from django.contrib import messages

class DatasetCreateForm(forms.Form):
    name = forms.CharField(max_length=50,required=True)
    connection_type = forms.ChoiceField(choices=helpers.build_choices(CONNECTION_TYPE_CHOICES))

class DatasetListView(View):
    def get(self,request,*args,**kwargs):
        model = Dataset.objects.all().order_by('id').reverse()
        return render(request,'base/dataset_list.html',{'dataset_list': model})

class DatasetCreateView(View):
    form_class = DatasetCreateForm
    template_name = 'base/dataset_create.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DatasetCreateForm(request.POST)
        if form.is_valid():
            a_data_set = Dataset(
                    name=form.cleaned_data.get('name'),
                    connection_type=form.cleaned_data('connection_type')
            )
            a_data_set.save()
            #my_redis = RedisDB(a_data_set.id)
            #my_redis.start_load()
            #load_dataset(a_data_set)
            messages.success(request, 'Dataset added.')
            return redirect('/dataset')
        else:
            return render(request, 'base/dataset_create.html', {'form': form})