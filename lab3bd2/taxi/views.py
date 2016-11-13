from django.shortcuts import render, redirect
from DatabaseManager import DB
import time

db = DB()


def main(request):
    msgs = []
    msgstr = ""
    if ('fromLength' in request.GET and request.GET['fromLength'] != '') or \
            ('toLength' in request.GET and request.GET['toLength'] != '') or \
            ('car_id' in request.GET and request.GET['car_id'] != '0'):
        start_time = time.time()
        orders = db.sort(request)
        time_res = time.time() - start_time
        if request.GET['car_id'] != '0':
            msgstr += 'by driver name\n'
        if request.GET['fromLength'] != '':
            msgstr += 'by length from ' + request.GET['fromLength'] + '\n'
        if request.GET['toLength'] != '':
            msgstr += 'by length to ' + request.GET['toLength'] + '\n'
        msgs.append(msgstr)
        msgs.append('search time : ' + str(time_res))
    else:
        orders = db.getOrderList()

    drivers = db.getDriverList()
    return render(request, 'main_page.html',
                  {'msgs': msgs, 'orders': orders[0:100], 'drivers': drivers, 'total': str(len(orders))})


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
        db.updateOrder({'order': id, 'driver': request.POST['driver'], 'customer': request.POST['customer'],
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
