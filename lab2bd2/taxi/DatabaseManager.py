import math
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.code import Code


class DB(object):
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test

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

    def getTopDriversAggregate(self):
        drivers =  list(self.db.order.aggregate(
            [{"$unwind": "$driver.name"}, {"$project": {"name": "$driver.name", "count": {"$add": [1]}}},
             {"$group": {"_id": "$name", "number": {"$sum": "$count"}}}, {"$sort": {"number": -1}}, {"$limit": 3}]))
        return drivers

    def mapTopDriver(self):
        mapper = Code("""
                            function() {
                                   var key = this.driver.name;
                                   var value = {count : 1};
                                   emit(key, value);
                            };
                            """)
        reducer = Code("""
                                function (key, values) {
                                    var count = 0;
                                    for(var i in values){
                                        count += values[i].count;
                                    }
                                    return {count: count};
                                };
                                """)
        result = self.db.order.map_reduce(mapper, reducer, "result")
        res = list(result.find())
        print res



    def mapAvPage(self):
        mapper = Code("""
                    function() {
                           var key = 1;
                           var value = {
                                         count: 1,
                                         total: this.total
                                       };
                           emit(key, value);
                    };
                    """)
        reducer = Code("""
                        function (key, values) {
                            var total = 0;
                            var count = 0;
                            for(var i in values){
                                count += values[i].count;
                                total += values[i].total;
                            }
                            return {total: total, count: count};
                        };
                        """)
        result = self.db.order.map_reduce(mapper, reducer, "result")
        res = list(result.find())
        print (res[0]['value']['total'] / res[0]['value']['count'])