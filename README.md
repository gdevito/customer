## Simple Backend with Rest endpoints for managing Customers

### API
#### when running customer server locally via ```python -m customer.server```, will default to port 8888
```shell
curl 127.0.0.1:8888/customer?uuid=<example uuid here>
```
##### Returns customer data for spefified query string uuid, as is reflected in postgres.

##### When testing
```shell
curl 127.0.0.1:8888/customer
```
##### Returns (uuid, username) key, value pairs for all users in customers db, for testing purposes
```shell
curl -i -H "Content-Type: application/json" -X PUT -d '{"username":"<name>", "address":"<address>", "income":"<income>"}' 127.0.0.1:8888/customer
```
##### Creates a new user within the customer database.  UUID and Create date supplied by the db.


### Design

The first decision made was to use python.  With the existing bindings for postgres and
mongo, simple to use tornado web server modules and a simple pytest-tornado testing
infrastructure, it was the fastest way for me to create the rest api's to do the job.
Then came mapping the problem set to a schema that could be used.  Determined easiest for
internal values like UUID and Date Created to be generated at the time of insert into postgres.
After a "customer" is inserted, a thread is run in the background which does the insert into
the mongodb collection, getting the customer as a dictionary response from get_by_uid_pg by doing
a lookup on the uuid created at insert time.  Thread startup time is negligible compared to
what could be a longer mongodb insert.  I chose to enable journaling to persist data consistently
to mongodb.  test_customers run by pytest, does quick checks to make sure running rest calls
are within the time expected. This setup revolves around a local, single server instance of mongodb.  In a distributed case, to ensure data is persisted across replicas, additional means could be taken.  One of these could be for force writes to disk in mongodb, likely at some interval ( maybe 30 seconds ) so as not to incur the 100ms slowdown per each distributed write.  Additional work to dockerize the instances to make for easier setup would also be something nice I'd like added.
