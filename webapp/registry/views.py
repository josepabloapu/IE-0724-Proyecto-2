from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from .models import Appointment, APPOINTMENT_HOURS, APPOINTMENT_PROVIDERS
from .forms import AppointmentForm, CustomUserCreationForm

def register_page(request):
    '''
    Register View.

    GET:
        Displays the form to register new user
    POST:
        Creates a user and redirects to the login page
    '''
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
    '''
    Login View.

    GET:
        Displays the form to login a user
    POST:
        Login and redirects to the home page
    '''
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
    '''
    Logout View.

    GET:
        Logout current logged user
    '''
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    '''
    Home View.

    GET:
        Display the main page of the application.
    '''
    context = {}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def appointment_list(request):
    '''
    Appointment List View.

    GET:
        Display all appointments. If an admin user is logged in,
        then results are not filtered by the user. Differently,
        if it is a normal user who is logged in,
        then he/she only can view his/her scheduled appointments.
    '''
    appointment_dict = {}
    now = datetime.now()
    for item in Appointment.objects.order_by('-datetime').all():
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
    context = {'appointment_dict': appointment_dict, }
    return render(request, 'appointment_list.html', context)


@login_required(login_url='login')
def appointment_read(request, pk=None):
    '''
    Appointment List View.

    GET:
        Display an appointment. If the user has enough privileges
        then he/she is able to see all the details.
    '''
    context = {}
    if pk is not None:
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404(f'Appointment with pk {pk} doesn\'t exist!')
        if (request.user.is_superuser or request.user == appointment.client):
            context = {'appointment': appointment}
            return render(request, 'appointment_read.html', context)
        else:
            messages.warning(request, f'User does not have permission to view this record.')
            return render(request, 'appointment_list.html', context)


@login_required(login_url='login')
def appointment_delete(request, pk=None):
    '''
    Appointment List View.

    GET:
        Remove an appointment. If the user has enough privileges
        then he/she is able to remove it.
    '''
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        raise Http404(f'Appointment with pk {pk} doesn\'t exist!')
    if (request.user.is_superuser or request.user == appointment.client):
        appointment.delete()
        messages.info(request, f'Record has been removed successfully.')
        return redirect('appointment_list')
    else:
        messages.warning(request, f'User does not have permission to remove this record.')
        return redirect('appointment_list')

@login_required(login_url='login')
def appointment_edit(request, pk=None):
    '''
    Appointment Edit View.

    GET:
        Displays a form to edit an appointment
    POST:
        Save appointment with the data provided
    '''
    context = {}
    if pk is not None:
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404(f'Appointment with pk {pk} doesn\'t exist!')


        if (appointment.client == request.user or request.user.is_superuser):
            # populate form
            edit_form = AppointmentForm(initial={'datetime': appointment.datetime.strftime('%Y-%m-%dT%H:%M'),
                                                 'provider': appointment.provider,
                                                 'client': appointment.client,
                                                 'province': appointment.province,
                                                 'latitude': appointment.latitude,
                                                 'longitude': appointment.longitude})

            # disable editing client for non admin users
            if not request.user.is_superuser:
                edit_form.fields['client'].widget.attrs['disabled'] = True

            # disable datetime and provider
            edit_form.fields['datetime'].widget.attrs['disabled'] = True
            edit_form.fields['provider'].widget.attrs['disabled'] = True

            if request.method == "POST":
                filled_form = AppointmentForm(request.POST, instance=appointment)
                # if not admin force not to change the client
                if not request.user.is_superuser:
                    filled_form.data._mutable = True
                    filled_form.data['client'] = request.user
                    filled_form.data._mutable = False

                # populate values that cannot be changed in the form
                filled_form.data._mutable = True
                filled_form.data['datetime'] = appointment.datetime
                filled_form.data['provider'] = appointment.provider
                filled_form.data['hour_of_day'] = appointment.hour_of_day
                filled_form.data['day_of_week'] = appointment.day_of_week
                filled_form.data['day_of_month'] = appointment.day_of_month
                filled_form.data['day_of_year'] = appointment.day_of_year
                filled_form.data['week_of_month'] = appointment.week_of_month
                filled_form.data['week_of_year'] = appointment.week_of_year
                filled_form.data['month'] = appointment.month
                filled_form.data['year'] = appointment.year
                filled_form.data._mutable = False

                new_appointment = filled_form.save()
                messages.info(request, f'Appointment ({new_appointment.pk}) was successfully updated.')
                return redirect('appointment_list')

            # send data to the template
            context = {"appointmentform": edit_form, 'appointment': appointment}
            return render(request, "appointment_edit.html", context)

        else:
            messages.warning(request, f'User does not have permission to view this record.')
            return render(request, 'appointment_list.html', context)


@login_required(login_url='login')
def appointment_new(request):
    '''
    Appointment New View.

    GET:
        Displays a form to create an appointment. Before rendering the view
        the app computes which is the next day with appointments available and
        which are the available spaces in the upcoming days. (Default is set to the upcoming 10 days)
    POST:
        Save appointment with the data provided
    '''

    def get_appointments_status_per_provider_per_date(provider, date):
        '''
        Aux function
            From the provided data, it returns the availability status of the appointment within a single day.

            @param [in] provider    select the provider from APPOINTMENT_PROVIDERS
            @param [in] date        select the datetime

            @return status          an array of type dictionary with 3 properties (provider, date, available)
        '''
        appointments = Appointment.objects.filter(provider=provider, year=date.year, month=date.month, day_of_month=date.day)
        status = {}
        for hour in APPOINTMENT_HOURS:
            status[hour[0]] = {"available": True, "provider": provider, "date": date.replace(hour=hour[0], minute=0).strftime('%Y-%m-%dT%H:%M')}
        for appointment in appointments:
            for hour in APPOINTMENT_HOURS:
                if appointment.hour_of_day == hour[0]:
                    status[hour[0]]['available'] = False
        return status

    def get_next_appointments_status_per_provider(provider, date, days_limit=9):
        '''
        Aux function
            From the provided data, it returns the availability status of the appointment within a group of days.
            This group starts from a certain day (D) until (D+days_limit)

            @param [in] provider    select the provider from APPOINTMENT_PROVIDERS
            @param [in] date        select the datetime
            @param [in] days_limit  determines the size of the group of days

            @return status          an array of type array of dictionaries with 3 properties (provider, date, available)
        '''
        counter = -1
        status = {}
        ref_date = date - timedelta(days=1)
        while counter < days_limit:
            ref_date = ref_date + timedelta(days=1)
            weekday = ref_date.weekday()
            if (weekday < 5):
                status[f"{ref_date.strftime('%a')}-{ref_date.day}"] = get_appointments_status_per_provider_per_date(provider, ref_date)
                counter = counter + 1
        return status

    def get_appointments_status_per_date(date):
        '''
        Aux function
            From the provided data, it returns the availability status of the appointment within a group of days and
            all available providers.

            @param [in] date        select the datetime

            @return status          an array of type array of array of dictionaries with 3 properties (provider, date, available)
        '''
        status = {}
        for provider in APPOINTMENT_PROVIDERS:
            status[provider[0]] = get_next_appointments_status_per_provider(provider[0], date)
        return status

    def get_next_appointment_available_date(date):
        '''
        Aux function
            Get the next availalbe day to schedule an appointment

            @param [in] date        select the datetime

            @return date            datetime instance of the next available day
        '''
        ref_date = date - timedelta(days=1)
        available_date_search = True
        while available_date_search:
            ref_date = ref_date + timedelta(days=1)
            if ref_date.weekday() < 5:
                appointments = Appointment.objects.filter(year=ref_date.year, month=ref_date.month, day_of_month=ref_date.day)
                if len(appointments) < len(APPOINTMENT_HOURS) * len(APPOINTMENT_PROVIDERS):
                    available_date_search = False
        return ref_date

    def check_appointment_availability(provider, datetime):
        '''
        Aux function
            Check if a day in available with the selected provider

            @param [in] provider    select the provider from APPOINTMENT_PROVIDERS
            @param [in] datetime    select the datetime

            @return bool            return whether the day is available or not
        '''
        appointment = Appointment.objects.filter(provider=provider, year=datetime.year, month=datetime.month, day_of_month=datetime.day, hour_of_day=datetime.hour)
        if len(appointment) == 0:
            return True
        else:
            return False

    # generate the availability matrix (day-provider)
    today = datetime.today()
    next_day = get_next_appointment_available_date(date=today)
    appointment_status = get_appointments_status_per_date(date=next_day)

    # compute the columns of the available dates table
    days = []
    for office in appointment_status:
        for day in appointment_status[office]:
            days.append(day)
        break

    # get query params from the url
    query_datetime = request.GET.get('datetime', today.strftime('%Y-%m-%dT%H:%M'))
    query_provider = request.GET.get('provider', None)

    # init the form
    new_form = AppointmentForm(initial={'datetime': query_datetime, 'provider': query_provider, 'client': request.user, 'latitude': 0.0, 'province': 'SJ', 'longitude': 0.0})

    # if user is not admin, then he/she only can assign an appointment for him/her
    if not request.user.is_superuser:
        new_form.fields['client'].widget.attrs['disabled'] = True

    # if HTTP request is POST
    if request.method == "POST":
        # create an Appointment object from the POST data
        filled_form = AppointmentForm(request.POST)

        # if not admin force not to change the client
        if not request.user.is_superuser:
            filled_form.data._mutable = True
            filled_form.data['client'] = request.user
            filled_form.data._mutable = False

        # custom validation, check if the datetime is valid
        error = 0
        date = datetime.strptime(filled_form.data['datetime'], '%Y-%m-%dT%H:%M')
        date = date.replace(minute=0, second=0, microsecond=0)

        # check if date is witch Mon-Fri
        if (date.weekday() >= 5):
            error = 1
            messages.warning(request, f"Invalid day provided ({date.strftime('%a')}), make sure it is a working day.")

        # check if the hour match with the available APPOINTMENT_HOURS
        hour = []
        for hour_tuple in APPOINTMENT_HOURS:
            hour.append(hour_tuple[0])
        if (date.hour not in hour):
            error = 1
            messages.warning(request, f"Invalid hour provided ({date.hour}), make sure it is a valid working hour.")

        # check if date is already taken
        if check_appointment_availability(filled_form.data['provider'], date) == False:
            error = 1
            messages.warning(request, f"This date is already taken. Provider: {filled_form.data['provider']}, Date: {date}")

        # continue if valid
        if (error == 0):
            # populate values that cannot be changed in the form
            filled_form.data._mutable = True
            filled_form.data['datetime'] = date
            filled_form.data['hour_of_day'] = date.hour
            filled_form.data['day_of_week'] = date.weekday()
            filled_form.data['day_of_month'] = date.day
            filled_form.data['day_of_year'] = date.timetuple().tm_yday
            filled_form.data['week_of_month'] = date.isocalendar()[1] - date.replace(day=1).isocalendar()[1] + 1
            filled_form.data['week_of_year'] = date.isocalendar()[1]
            filled_form.data['month'] = date.month
            filled_form.data['year'] = date.year
            filled_form.data._mutable = False

            # save appointment
            new_appointment = filled_form.save()
            messages.success(request, f"Appointment for client ({new_appointment.client}) at ({new_appointment.datetime.strftime('%Y-%m-%d %H:%M')}) has been created.")
            return redirect('appointment_list')

    context = {"appointmentform": new_form, "appointment_status": appointment_status, "days": days}
    return render(request, "appointment_new.html", context)
