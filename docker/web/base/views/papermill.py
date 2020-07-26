from django.views.generic import View
from django.shortcuts import redirect
import papermill


# this is the start of a more general rest schema for pagemill created jupyter notebooks
class PapermillView(View):
    def get(self, request, *args, **kwargs):
        template_name = args[0]
        object_id = args[1]
        option = args[2]
        papermill.execute_notebook(
            'Notebooks/templates/' + template_name + '.ipynb',
            'Notebooks/dynamic/' + request.session._session_key + '.ipynb',
            parameters=dict(objectIDParameter=object_id, option=option)
        )
        return redirect('http://' + request.get_host().split(':')[
            0] + ':8080/lab/tree/dynamic/' + request.session._session_key + '.ipynb')
