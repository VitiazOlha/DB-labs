from django.shortcuts import render, redirect
from DatabaseManager import DB

db = DB()


def main(request):
    db.mapTopDriver()
    db.mapAvPage()
    orders = db.getOrderList()
    return render(request, 'main_page.html', {'orders': orders})


def remove(request, id):
    db.removeOrder(id)
    return redirect('/')


def edit(request, id):
    if request.method == 'GET':
        address = db.getAddressList()
        drivers = db.getDriverList()
        customers = db.getClientList()
        order = db.getOrder(id)
        return render(request, 'edit_page.html',
                      {'address': address, 'drivers': drivers, 'customers': customers, 'order': order})
    elif request.method == 'POST':
        db.updateOrder({'order': id,'driver': request.POST['driver'], 'customer': request.POST['customer'],
                      'address_from': request.POST['address_from'],
                      'y_from': request.POST['y_from'], 'address_to': request.POST['address_to'],
                      'y_to': request.POST['y_to'], 'data': request.POST['data']})
        return redirect('/')


def add(request):
    if request.method == 'GET':
        address = db.getAddressList()
        drivers = db.getDriverList()
        customers = db.getClientList()
        return render(request, 'add_page.html', {'address': address, 'drivers': drivers, 'customers': customers})
    elif request.method == 'POST':
        db.saveOrder({'driver': request.POST['driver'], 'customer': request.POST['customer'],
                      'address_from': request.POST['address_from'],
                      'y_from': request.POST['y_from'], 'address_to': request.POST['address_to'],
                      'y_to': request.POST['y_to'], 'data': request.POST['data']})
        return redirect('/')


def topdrivers(request):
    drivers = db.getTopDriversAggregate()
    return render(request, 'drivers_top_page.html', {'drivers': drivers})
