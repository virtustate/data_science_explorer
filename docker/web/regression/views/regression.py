from datetime import datetime
from django import forms
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from regression.models import Regression
from regression.models import Regression
from base.models.dataset import Dataset
from sklearn.linear_model import LinearRegression
from base.redis_db import RedisDB


class RegressionCreateForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    dataset = forms.ModelChoiceField(queryset=Dataset.objects.all())
    dependent_column = forms.ChoiceField()
    independent_columns = forms.MultipleChoiceField()

    def clean(self):
        super(RegressionCreateForm, self).clean()
        del self.errors["independent_columns"]
        del self.errors["dependent_column"]


class RegressionListView(View):
    def get(self, request, *args, **kwargs):
        model = Regression.objects.all().order_by("id").reverse()
        return render(
            request, "regression/regression_list.html", {"regression_list": model}
        )


class RegressionCreateView(View):
    form_class = RegressionCreateForm
    template_name = "regression/regression_create.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            a_regression = Regression(
                name=form.cleaned_data["name"],
                created=datetime.now(),
                dataset=form.cleaned_data["dataset"],
                independent_columns=request.POST.getlist("independent_columns"),
                dependent_column=form.data["dependent_column"],
            )
            # do regression
            my_redis = RedisDB(a_regression.dataset.id)
            df = my_redis.get_df('dataframe')
            lr = LinearRegression()
            lr.fit(df[a_regression.independent_columns], df[a_regression.dependent_column])
            a_regression.set_results(lr)
            a_regression.save()
            messages.success(request, "Regression added.")
            return redirect("/regression")
        else:
            return render(request, self.template_name, {"form": form})


class RegressionDeleteView(View):
    def get(self, request, *args, **kwargs):
        regression_id = kwargs["pk"]
        Regression.objects.filter(id=regression_id).delete()
        messages.success(request, "Regression deleted.")
        return redirect("/regression")


class RegressionViewView(View):
    def get(self, request, *args, **kwargs):
        regression_id = kwargs["pk"]
        html = f"regression_id: {regression_id}<br/>"
        return render(request, "regression/regression_view.html", {"html": html})
