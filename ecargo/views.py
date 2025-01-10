from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import LoginForm, UserCreationForm
from .models import Members, Trucking




def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form  = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    context = {'loginform': form}
    return render(request, 'user-login.html', context=context)

def user_register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    context = {'registerform': form}
    return render(request, 'user-register.html', context=context)

def dashboard(request):
    return render(request, 'dashboard.html', {})

@login_required(login_url='my-login')
def all_trucks(request):
    trucks = Trucking.objects.all()
    context = {'trucks': trucks}
    return render(request, 'ecargo/all-trucks.html', context=context)

    # if no day is selected, show all trucks
    if selected_day == 'All':
        trucks = trucks
    # otherwise, filter by day
    else:
        trucks = trucks.filter(day=selected_day)

@login_required(login_url='my-login')
def all_members(request):
    # Get query parameters
    search_query = request.GET.get('q', '')  # Get search query
    sort_order = request.GET.get('sort', 'asc')  # Default sort order
    per_page = int(request.GET.get('per_page', 8))  # Default items per page

    # Fetch and filter members based on search_query
    members = Members.objects.all()

    # Apply search filter
    if search_query:
        members = members.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    # Apply sorting (if applicable)
    if sort_order == 'asc':
        members = members.order_by('first_name')
    else:
        members = members.order_by('-first_name')

    # Paginate members
    paginator = Paginator(members, per_page)  # Create paginator
    page = request.GET.get('page', 1)  # Get current page number

    try:
        members_page = paginator.page(page)  # Get the requested page
    except PageNotAnInteger:
        members_page = paginator.page(1)  # Default to the first page
    except EmptyPage:
        members_page = paginator.page(paginator.num_pages)  # Default to the last page

    # Context for rendering
    context = {
        'members': members_page,
        'search_query': search_query,
        'sort_order': sort_order,
        'per_page': per_page,
    }
    return render(request, 'ecargo/all-members.html', context=context)

@login_required(login_url='my-login')
def all_trucks(request):
    # Get query parameters
    search_query = request.GET.get('q', '')  # Get search query
    selected_day = request.GET.get('day', 'All')  # Default to 'All'
    sort_order = request.GET.get('sort', 'asc')  # Default sort order
    per_page = int(request.GET.get('per_page', 8))  # Default items per page

    # Fetch and filter trucks based on search_query and selected_day
    trucks = Trucking.objects.all()
    # Filter by search_query (applies to destination, day, or departure_time)
    if search_query:
        trucks = trucks.filter(
            Q(destination__icontains=search_query) |
            Q(day__icontains=search_query) |
            Q(origin__icontains=search_query) |
            Q(departure_time__icontains=search_query)  # Search times as strings (format HH:MM)
    )
        
        
    # Sort trucks
    if sort_order == 'desc':
        trucks = trucks.order_by('-departure_time')
    else:
        trucks = trucks.order_by('departure_time')

    # Paginate trucks
    paginator = Paginator(trucks, per_page)  # Create paginator
    page = request.GET.get('page', 1)  # Get current page number

    try:
        trucks_page = paginator.page(page)  # Get the requested page
    except PageNotAnInteger:
        trucks_page = paginator.page(1)  # Default to the first page
    except EmptyPage:
        trucks_page = paginator.page(paginator.num_pages)  # Default to the last page

    # Return rendered page with context
    return render(request, 'ecargo/all-trucks.html', {
        'trucks': trucks_page,
        'search_query': search_query,
        'selected_day': selected_day,
        'sort_order': sort_order,
        'per_page': per_page,
    })

@login_required(login_url='my-login')
def single_truck(request, id):
    truck = Trucking.objects.get(id=id)
    context = {'truck': truck}
    return render(request, 'ecargo/single-truck.html', context=context)

@login_required(login_url='my-login')
def single_member(request, id):
    member = Members.objects.get(id=id)
    context = {'member': member}
    return render(request, 'ecargo/single-member.html', context=context)

@login_required(login_url='my-login')
def add_truck(request):
    if request.method == 'POST':
        truck = Trucking()
        truck.day = request.POST.get('day')
        truck.air_line_code = request.POST.get('air_line_code')
        truck.flight_number = request.POST.get('flight_number')
        truck.departure_time = request.POST.get('departure_time')
        truck.distance = request.POST.get('distance')
        truck.travel_time = request.POST.get('travel_time')
        truck.origin = request.POST.get('origin')
        truck.destination = request.POST.get('destination')
        truck.operator = request.POST.get('operator')
        truck.status = request.POST.get('status')

        truck.save()
        return redirect('all-trucks')

    return render(request, 'ecargo/add-truck.html', {})

@login_required(login_url='my-login')
def add_member(request):
    if request.method == 'POST':
        member = Members()
        member.first_name = request.POST.get('first_name')
        member.middle_name = request.POST.get('middle_name')
        member.last_name = request.POST.get('last_name')
        member.email = request.POST.get('email')
        member.phone = request.POST.get('phone')
        member.function = request.POST.get('function')

        member.save()
        return redirect('all-members')

    return render(request, 'ecargo/add-member.html', {})

@login_required(login_url='my-login')
def update_truck(request, id):
    truck = Trucking.objects.get(id=id)
    if request.method == 'POST':
        truck.day = request.POST.get('day')
        truck.air_line_code = request.POST.get('air_line_code')
        truck.flight_number = request.POST.get('flight_number')
        truck.departure_time = request.POST.get('departure_time')
        truck.distance = request.POST.get('distance')
        truck.travel_time = request.POST.get('travel_time')
        truck.origin = request.POST.get('origin')
        truck.destination = request.POST.get('destination')
        truck.operator = request.POST.get('operator')
        truck.status = request.POST.get('status')

        truck.save()
        return redirect('all-trucks')

    context = {'truck': truck}
    return render(request, 'ecargo/update-truck.html', context=context)
@login_required(login_url='my-login')
def update_member(request, id):
    member = Members.objects.get(id=id)
    if request.method == 'POST':
        member.first_name = request.POST.get('first_name')
        member.middle_name = request.POST.get('middle_name')
        member.last_name = request.POST.get('last_name') or ''  # Avoid NOT NULL constraint
        member.email = request.POST.get('email')
        member.phone = request.POST.get('phone')
        member.function = request.POST.get('function')

        member.save()
        return redirect('all-members')

    context = {'member': member}
    return render(request, 'ecargo/update-member.html', context=context)

@login_required(login_url='my-login')
def delete_truck(request, id):
    truck = Trucking.objects.get(id=id)
    truck.delete()
    return redirect('all-trucks')

@login_required(login_url='my-login')
def delete_member(request, id):
    member = Members.objects.get(id=id)
    member.delete()
    return redirect('all-members')
@login_required(login_url='my-login')
def logout_view(request):
    logout(request)
    return redirect('user-login') 