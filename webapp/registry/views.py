from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Asset
from .forms import AssetForm, CustomUserCreationForm
# Create your views here.


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CustomUserCreationForm()
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, f"Account was created for {user}")
                return redirect("login")
        context = {'form': form}
        return render(request, "register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'home.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def assets_delete(request, pk=None):
    try:
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        raise Http404(f'Asset with pk {pk} doesn\'t exist!')
    asset.delete()
    return redirect('asset_list')


@login_required(login_url='login')
def assets_new(request):
    new_form = AssetForm(initial={'owner': request.user, 'latitude': 0.0, 'longitude': 0.0})
    if not request.user.is_superuser:
        new_form.fields['owner'].widget.attrs['disabled'] = True
    if request.method == "POST":
        filled_form = AssetForm(request.POST)
        if not request.user.is_superuser:
            filled_form.data._mutable = True
            filled_form.data['owner'] = request.user
            filled_form.data._mutable = False
        new_asset = filled_form.save()
        new_pk = new_asset.pk
        note = f"Asset object with pk: {new_pk} was successfully created."
    else:
        note = "Please proceed to add a new asset."

    context = {"note": note, "assetform": new_form}
    return render(request, "assets_new.html", context)
