from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
from car_dealer_portal.models import *
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'customer/login.html')
    else:
        return render(request, 'customer/home_page.html')

def login(request):
    return render(request, 'customer/login.html')

    
def home_page(request):
    return render(request, 'customer/home_page.html')


def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'customer/home_page.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            customer = Customer.objects.get(user = user)
        except:
            customer = None
        if customer is not None:
            auth.login(request, user)
            return render(request, 'customer/home_page.html')
        else:
            return render(request, 'customer/login_failed.html')

def logout_view(request):
    auth.logout(request)
    return render(request, 'customer/login.html')

def register(request):
    return render(request, 'customer/register.html')

def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    mobile = request.POST['mobile']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'customer/registration_error.html')
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        customer = Customer(user = user, mobile = mobile, area = area)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        customer = Customer(user = user, mobile = mobile, area = area)

    customer.save()
    return render(request, 'customer/registered.html')

@login_required
def search(request):
    return render(request, 'customer/search.html')

@login_required
def search_results(request):
    capacity = request.POST['capacity']
    vehicles_list = []
    vehicles = Vehicles.objects.filter(capacity__gte=capacity, is_available=True)
    for car in vehicles:
        vehicle_dictionary = {
            'name': car.car_name,
            'color': car.color,
            'id': car.id,
            'city': car.area.city,
            'capacity': car.capacity,
            'description': car.description,
            'driver_name': car.driver_name,
            'driver_contact': car.driver_contact,
        }
        vehicles_list.append(vehicle_dictionary)
    request.session['vehicles_list'] = vehicles_list
    
    return render(request, 'customer/search_results.html', {'vehicles_list': vehicles_list})


@login_required
def rent_vehicle(request):
    id = request.POST['id']
    vehicle = Vehicles.objects.get(id=id)
    cost_per_day = int(vehicle.capacity) * 50
    return render(request, 'customer/confirmation.html', {'vehicle': vehicle, 'cost_per_day': cost_per_day})

@login_required
def confirm(request):
    cl=request.POST['cl']
    mob=request.POST['mob']
    em=request.POST['em']
    vehicle_id = request.POST['id']
    username = request.user
    user = User.objects.get(username = username)
    
    days = request.POST['days']
    reservation_date=request.POST['reservation_date']

    status=request.POST['status']
    vehicle = Vehicles.objects.get(id = vehicle_id)
    if vehicle.is_available:
        car_dealer = vehicle.dealer
        rent = (int(vehicle.capacity))*50*(int(days))
        car_dealer.wallet += rent
        car_dealer.save()
        try:
            order = Orders(cl=cl, mob=mob, em=em, vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days,reservation_date=reservation_date,status=status)
            order.save()
        except:
            order = Orders.objects.get(cl=cl, mob=mob, em=em, vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days,reservation_date=reservation_date,status=status)
        vehicle.is_available = False
        vehicle.save()
        return render(request, 'customer/confirmed.html', {'order':order})
    else:
        return render(request, 'customer/order_failed.html')

@login_required
def manage(request):
    order_list = []
    user = User.objects.get(username = request.user)
    try:
        orders = Orders.objects.filter(user = user)
    except:
        orders = None
    if orders is not None:
        for o in orders:
            if o.is_complete == False:
                order_dictionary = {'cl':o.cl,'mob':o.mob,'em':o.em,'id':o.id,'rent':o.rent, 'vehicle':o.vehicle,  'days':o.days, 'reservation_date':o.reservation_date, 'status':o.status, 'car_dealer':o.car_dealer}
                order_list.append(order_dictionary)
    return render(request, 'customer/manage.html', {'od':order_list})

@login_required
def update_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    vehicle = order.vehicle
    vehicle.is_available = True
    vehicle.save()
    car_dealer = order.car_dealer
    car_dealer.wallet -= int(order.rent)
    car_dealer.save()
    order.delete()
    cost_per_day = int(vehicle.capacity)*50
    return render(request, 'customer/confirmation.html', {'vehicle':vehicle}, {'cost_per_day':cost_per_day})

@login_required
def delete_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    car_dealer = order.car_dealer
    car_dealer.wallet -= int(order.rent)
    car_dealer.save()
    vehicle = order.vehicle
    vehicle.is_available = True
    vehicle.save()
    order.delete()
    return HttpResponseRedirect('/customer_portal/manage/')
