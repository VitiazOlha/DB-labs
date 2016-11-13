import math
import pickle
from pymongo import MongoClient
import redis
from bson.objectid import ObjectId


class DB(object):
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test
        self.r = redis.StrictRedis()
        #self.r.set('version', 0)

    def getOrderList(self):
        orders = [order for order in self.db.order.find()]
        return orders

    def getAddressList(self):
        addresses = [address for address in self.db.address.find()]
        for address in addresses:
            address['x'] = int(address['x'])
        return addresses

    def getDriverList(self):
        drivers = [driver for driver in self.db.driver.find()]
        return drivers

    def getClientList(self):
        clients = [client for client in self.db.customer.find()]
        return clients

    def getOrder(self, id):
        order = self.db.order.find_one({'_id': ObjectId(id)})
        return order

    def removeOrder(self, id):
        self.db.order.delete_one({'_id': ObjectId(id)})
        self.r.incr('version')

    def saveOrder(self, info):
        driver = self.db.driver.find_one({'_id': ObjectId(info['driver'])})
        customer = self.db.customer.find_one({'_id': ObjectId(info['customer'])})
        address_from = self.db.address.find_one({'_id': ObjectId(info['address_from'])})
        address_to = self.db.address.find_one({'_id': ObjectId(info['address_to'])})
        total = int(math.fabs(int(address_from['x']) - int(address_to['x'])) + math.fabs(
            int(info['y_from']) - int(info['y_to'])))
        order = {'driver': driver, 'customer': customer, 'address_from': address_from, 'address_to': address_to,
                 'y_from': int(info['y_from']), 'y_to': int(info['y_to']), 'total': total, 'data': info['data']}
        self.db.order.insert(order)
        self.r.incr('version')

    def updateOrder(self, info):
        driver = self.db.driver.find_one({'_id': ObjectId(info['driver'])})
        customer = self.db.customer.find_one({'_id': ObjectId(info['customer'])})
        address_from = self.db.address.find_one({'_id': ObjectId(info['address_from'])})
        address_to = self.db.address.find_one({'_id': ObjectId(info['address_to'])})
        total = int(math.fabs(int(address_from['x']) - int(address_to['x'])) + math.fabs(
            int(info['y_from']) - int(info['y_to'])))
        order = {'driver': driver, 'customer': customer, 'address_from': address_from, 'address_to': address_to,
                 'y_from': int(info['y_from']), 'y_to': int(info['y_to']), 'data': info['data'],
                 'total': total}
        self.db.order.update_one({'_id': ObjectId(info['order'])}, {'$set': order})
        self.r.incr('version')

    def sort(self, request):
        req = str(request).partition('&')[2]
        if self.r.exists(req) != 0 and self.r.hget(req, 'version') == self.r.get('version'):
            order = pickle.loads(self.r.hget(req, 'res'))
        else:
            query = {}
            if request.GET['fromLength'] != '' or request.GET['toLength'] != '':
                query["total"] = {}
                if request.GET['fromLength'] != '':
                    query["total"]['$gte'] = int(request.GET['fromLength'])
                if request.GET['toLength'] != '':
                    query["total"]['$lte'] = int(request.GET['toLength'])
            if request.GET['car_id'] != '0':
                query["driver._id"] = ObjectId(request.GET['car_id'])
            order = list(self.db.order.find(query))
            self.r.hmset(req, {'res': pickle.dumps(order), 'version': self.r.get('version')})
        return list(order)
