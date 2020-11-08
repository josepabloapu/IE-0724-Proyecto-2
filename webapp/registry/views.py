from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Asset
# Create your views here.


def home(request):
    context = {}
    return render(request, 'home.html', context)


def assets_list(request):
    asset_dict = {}
    for item in Asset.objects.all():
        if (item.owner == request.user or request.user.is_superuser):
            asset_dict[item.pk] = {
                'pk': item.pk,
                'alias': item.alias,
                'province': item.province,
                'category': item.category,
                'latitude': item.latitude,
                'longitude': item.longitude,
                'owner': item.owner,
            }
    context = {'asset_dict': asset_dict, }
    return render(request, 'assets_list.html', context)


def assets_read(request, pk=None):
    if pk is not None:
        try:
            asset = Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            raise Http404(f'Asset with pk {pk} doesn\'t exist!')
        context = {'asset': asset}
        return render(request, 'assets_read.html', context)
    else:
        context = {}
        return render(request, 'assets_read.html', context)


def assets_delete(request, pk=None):
    try:
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        raise Http404(f'Asset with pk {pk} doesn\'t exist!')
    asset.delete()
    return redirect('asset_list')