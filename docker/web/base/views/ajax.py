from django.http import JsonResponse
from base.models.dataset import Dataset


def ajax_get_dataset_columns(request):
    dataset_id = request.GET.get('dataset_id')
    if dataset_id == None or dataset_id == '':
        return JsonResponse([], safe=False)
    a_dataset = Dataset.objects.filter(id=dataset_id)[0]
    return JsonResponse(a_dataset.columns, safe=False)
