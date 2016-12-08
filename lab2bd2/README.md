## About
Assignment #2 project for databases 5th semester course: web-application development using document-oriented database MongoDB.

## Goals
* Use subject area of Assignment #2 from semester 4
* Develop MongoDB schema design
* Implement database layer using `pymongo`
* Use map/reduce and aggregation framework

## Aggregate function
```js
self.db.order.aggregate([
            {"$unwind": "$driver.name"}, 
            {"$project": {
              "name": "$driver.name", 
              "count": {"$add": [1]}
            }},
            {"$group": {
              "_id": "$name", 
              "number": {"$sum": "$count"}
            }}, 
            {"$sort": {"number": -1}}, 
            {"$limit": 3}
])

```
## Map/reduce 
```py
mapper = Code("""
              function() {
                var key = this.driver.name;
                var value = {
                  count : 1
                };
                emit(key, value);
              };
              """)
reducer = Code("""
              function (key, values) {
                  var count = 0;
                  for(var i in values) {
                      count += values[i].count;
                  }
                  return {count: count};
              };
              """)
result = self.db.order.map_reduce(mapper, reducer, "result")
```

```py
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

```
