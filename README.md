## Simple Backend with Rest endpoints for managing Customers

### API
#### when running customer server locally via $ python -m customer.server, will default to port 8888
```shell
curl 127.0.0.1:8888/customer?uuid=<example uuid here>

Returns customer data for spefified query string uuid, as is reflected in postgres.

When testing
curl 127.0.0.1:8888/customer
Return (uuid, username) key, value pairs for all users in customers db, for testing purposes

curl -i -H "Content-Type: application/json" -X PUT -d '{"username":"<name>", "address":"<address>", "income":"<income>"}' 127.0.0.1:8888/customer

Create a new user within the customer database.  UUID and Create date supplied by the db.
```
