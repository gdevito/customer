## Simple Backend with Rest endpoints for managing Customers

### API

```shell
curl url:port/customer?uuid=<example uuid here>

Returns customer data for spefified query string uuid, as is reflected in postgres.

curl -i -H "Content-Type: application/json" -X PUT -d '{"username":"<name>", "address":"<address>", "income":"<income>"}' url:port/customer

Create a new user within the customer database.  UUID and Create date supplied by the db.
```
