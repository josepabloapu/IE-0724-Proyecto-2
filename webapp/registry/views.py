from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import datetime
from .models import Appointment
from .forms import AppointmentForm, CustomUserCreationForm
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
def appointment_list(request):
    appointment_dict = {}
    now = datetime.datetime.now()
    for item in Appointment.objects.all():
        if abs(now.year-item.datetime.year) <= 1:
            if (item.client == request.user or request.user.is_superuser):

                appointment_dict[item.pk] = {
                    'pk': item.pk,
                    'datetime': item.datetime,
                    'provider': item.provider,
                    'client': item.client,
                    'province': item.province,
                    'latitude': item.latitude,
                    'longitude': item.longitude,
                }


    busqueda = request.GET.get("buscar", "")
    print(busqueda)
    propiedades = Appointment.objects.all()
    if busqueda:
        propiedades = Appointment.objects.filter(
            Q(datetime__icontains=busqueda) |
            Q(provider__icontains=busqueda) |
            Q(client__icontains=busqueda)
        )
    context = {'appointment_dict': appointment_dict, 'propiedades': propiedades}
    return render(request, 'appointment_list.html', context)


@login_required(login_url='login')
def appointment_read(request, pk=None):



    if pk is not None:
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404(f'Appointment with pk {pk} doesn\'t exist!')
        context = {'appointment': appointment}
        return render(request, 'appointment_read.html', context)
    else:
        context = {}
        return render(request, 'appointment_read.html', context)









@login_required(login_url='login')
def appointment_edit(request, pk=None):
    if pk is not None:
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404(f'Appointment with pk {pk} doesn\'t exist!')
        if (appointment.client == request.user or request.user.is_superuser):

            edit_form = AppointmentForm(initial={'datetime': appointment.datetime.strftime('%Y-%m-%dT%H:%M'),
                                                'provider': appointment.provider,
                                                'client': appointment.client,
                                                'province': appointment.province,
                                                'latitude': appointment.latitude,
                                                'longitude': appointment.longitude})
            if not request.user.is_superuser:
                edit_form.fields['client'].widget.attrs['disabled'] = True
            if request.method == "POST":
                filled_form = AppointmentForm(request.POST, instance=appointment)
                if not request.user.is_superuser:
                    filled_form.data._mutable = True
                    filled_form.data['client'] = request.user
                    filled_form.data._mutable = False
                new_appointment = filled_form.save()
                new_pk = new_appointment.pk
                note = f"Appointment object with pk: {new_pk} was successfully created."
                return redirect('appointment_list')
            else:
                note = "Please proceed to add a new appointment."

            context = {"note": note, "appointmentform": edit_form, 'appointment': appointment}
            return render(request, "appointment_edit.html", context)

        else:
            raise Http404(f'User cannot view appointment with pk {pk}!')
    else:
        context = {}
        return render(request, 'appointment_read.html', context)


@login_required(login_url='login')
def appointment_delete(request, pk=None):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        raise Http404(f'Appointment with pk {pk} doesn\'t exist!')
    appointment.delete()
    return redirect('appointment_list')


@login_required(login_url='login')
def appointment_new(request):
    # fill default values
    today = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M')
    new_form = AppointmentForm(initial={'datetime': today, 'client': request.user, 'latitude': 0.0, 'longitude': 0.0})

    # if user is not admin, then he/she only can assign an appointment for him/her
    if not request.user.is_superuser:
        new_form.fields['client'].widget.attrs['disabled'] = True

    # if HTTP request is POST
    if request.method == "POST":
        filled_form = AppointmentForm(request.POST)
        if not request.user.is_superuser:
            filled_form.data._mutable = True
            filled_form.data['client'] = request.user
            filled_form.data._mutable = False

        # sanitize datetime for work hours
        error = 0
        date = datetime.datetime.strptime(filled_form.data['datetime'], '%Y-%m-%dT%H:%M')
        date = date.replace(second=0, microsecond=0)

        if (date.minute >= 30):
            date = date.replace(minute=30)
        else:
            date = date.replace(minute=0)

        if (date.weekday() >= 5):
            error = 1
            messages.warning(request, f"Day: {date.weekday() + 1}")
            messages.warning(request, "Invalid day provided, make sure it is a working day. Mon-Fri")

        if (date.hour < 8 or date.hour > 16):
            error = 1
            messages.warning(request, f"Hour: {date.hour}")
            messages.warning(request, "Invalid hour provided, make sure it is a valid working hour. From 8:00 to 15:59")

        # continue if valid
        if (error == 0):
            filled_form.data._mutable = True
            filled_form.data['datetime'] = date
            filled_form.data._mutable = False

            #add time conflic logic

            new_appointment = filled_form.save()
            messages.success(request, f"Appointment for client {new_appointment.client} at {new_appointment.datetime} was successfully created.")

    context = {"appointmentform": new_form}
    return render(request, "appointment_new.html", context)
