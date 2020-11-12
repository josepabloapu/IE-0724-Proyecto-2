from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Asset
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from .forms import AssetForm
from django.contrib.auth import login, authenticate
# Create your views here.


def home(request):
    context = {}
    return render(request, 'home.html', context)


@login_required
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

@login_required
def new(request):
    new_form = AssetForm()
    if request.method == 'POST':
        filled_form = AssetForm(request.POST)
        if filled_form.is_valid():
            new_asset = filled_form.save()
            note = (
                'La propiedad con el pk: \'{}\' fue creada exitosamente!\n'
                'Nombre: {}'.format(
                    new_asset.pk, filled_form.cleaned_data['owner']
                )
            )
        else:
            note = 'Datos invalidos!'
        return render(
            request,
            'new_asset.html',
            {
                'AssetForm': new_form,
                'note': note
            }
        )

    else:
        return render(
            request,
            'new_asset.html',
            {
                'AssetForm': new_form,
            }
        )


def registro_usuario(request):

    data = {
        'form': CustomUserForm()
    }

    if request.method == 'POST':
        formulario = CustomUserForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            #Autenticar al usuario y redirigirlo al inicio
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(to='home')
    return render(request, 'registration/registrar.html', data)
