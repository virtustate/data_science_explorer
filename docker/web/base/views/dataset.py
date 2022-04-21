from django.views.generic import View
from django.shortcuts import render,redirect
from base.models.dataset import Dataset,CONNECTION_TYPE_CHOICES, DELIMTER_CHOICES
from django import forms
from base.redis_db import RedisDB
from django.contrib import messages
from datetime import datetime

class DatasetCreateForm(forms.Form):
    name = forms.CharField(max_length=50,required=True)
    connection_type = forms.ChoiceField(choices=CONNECTION_TYPE_CHOICES)
    file_upload = forms.FileField()
    delimiter = forms.ChoiceField(choices=DELIMTER_CHOICES)
    header = forms.BooleanField(required=False, initial=True)

class DatasetListView(View):
    def get(self,request,*args,**kwargs):
        model = Dataset.objects.all().order_by('id').reverse()
        my_redis=RedisDB()
        return render(request,'base/dataset_list.html',{'dataset_list': model, 'redis_metadata': my_redis.get_metadata()})

class DatasetCreateView(View):
    form_class = DatasetCreateForm
    template_name = 'base/dataset_create.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            a_data_set = Dataset(
                    name=form.cleaned_data['name'],
                    connection_type=form.cleaned_data['connection_type'],
                    created = datetime.now(),
                    delimiter = form.cleaned_data['delimiter'],
                    header = form.cleaned_data['header'],
            )
            a_data_set.save()
            columns = a_data_set.load_file_to_redis(form.cleaned_data['file_upload'].file)
            a_data_set.columns = columns
            a_data_set.save()
            messages.success(request, 'Dataset added.')
            return redirect('/dataset')
        else:
            return render(request, self.template_name, {'form': form})

class DatasetDeleteView(View):
    def get(self, request, *args, **kwargs):
        dataset_id = kwargs['pk']
        Dataset.objects.filter(id=dataset_id).delete()
        my_redis = RedisDB(dataset_id)
        my_redis.delete_db()
        messages.success(request, 'Dataset deleted.')
        return redirect('/dataset')

class DatasetViewView(View):
    def get(self, request, *args, **kwargs):
        dataset_id = kwargs['pk']
        my_redis = RedisDB(dataset_id)
        a_dataset = Dataset.objects.filter(id=dataset_id)[0]
        df = my_redis.get_df('dataframe')
        if df.shape[0] > 50:
            html = f'{df.head(10).to_html()}<br/>...<br/>{df.tail(10).to_html()}'
        else:
            html = df.to_html()
        html = f'shape: {df.shape}<br/>columns: {a_dataset.columns}</b><br/>{df.info()}{html}'
        return render(request, 'base/dataset_view.html', {'html': html})