import math
import random
import time

from pymongo import MongoClient

client = MongoClient()
db = client.test

db.order.remove()
driver = list(db.driver.find())
customer = list(db.customer.find())
address = list(db.address.find())

for i in range(0, 100000):
    order = {
        'driver': random.choice(driver),
        'customer': random.choice(customer),
        'address_from': random.choice(address),
        'address_to': random.choice(address),
        'y_from': random.randint(0, 150),
        'y_to': random.randint(0, 150),
        'data': time.strftime("%Y-%m-%dT%H:%M", time.gmtime(random.randint(1400000000, 1475000000)))
    }
    total = int(math.fabs(int(order['address_from']['x']) - int(order['address_to']['x']))
                + math.fabs(int(order['y_from']) - int(order['y_to'])))
    order["total"] = total
    db.order.insert(order)
