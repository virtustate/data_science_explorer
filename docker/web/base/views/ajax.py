from django.http import JsonResponse
from base.models.dataset import Dataset


def ajax_dataset_columns(request):
    dataset_id = request.GET.get('dataset_id')
    if dataset_id == 'none':
        return JsonResponse([], safe=False)
    a_dataset = Dataset.objects.filter(dataset_id=dataset_id)[0]
    return JsonResponse(a_dataset.columns, safe=False)
