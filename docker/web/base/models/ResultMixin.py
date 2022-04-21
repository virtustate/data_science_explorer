from django.db import models
import pickle
import base64


class ResultMixin(models.Model):
    """
    This mixin contains functionality to stuff a bunch of results into a Django text field named result.
    """
    class Meta:
        abstract = True

    result = models.TextField(default='')

    def get_results(self):
        if self.result == '' or self.result is None:
            return dict()
        # when switching to django2, needed to remove 'b' in front of result here
        if self.result[0] == 'b':
            self.result = self.result[1:]
        return pickle.loads(base64.b64decode(self.result))

    def set_results(self, results):
        self.result = base64.b64encode(pickle.dumps(results, 4))

    results = property(get_results, set_results)

    def add_results(self, key, value, breakout_member=None):
        results = self.get_results()
        if breakout_member is None:
            results[key] = value
        else:
            if key not in results.keys():
                results[key] = dict()
            results[key][breakout_member] = value
        self.results = results
