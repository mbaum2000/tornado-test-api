# Widget Inventory API Demo (using Tornado)

Sample API Application to explore the Tornado framework

## Setup

These steps use the `venv` module, which is available on Ubuntu in the `python3-venv` package.

```
# Checkout
git clone /path/to/repo/tornado-test-api.git
cd tornado-test-api/

# Virtualenv
python3 -m virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt

# Run
python3 run.py
```

## Running

Once running, the API will be accessible at http://localhost:8080/widget

## Environment

The application will use the following environment variables:
 * `DEBUG=1`: Turn on Tornado Application Debug
 * `DEBUG_SQL=1`: Turn on SQLAlchemy Query Echo
 * `PORT=8080`: Turn on SQLAlchemy Query Echo
 * `DB_FILENAME=sqlite:///widgets.db`: Specify a different SQLite Database

## API

`GET` `/widget`

Returns a list of Widgets:
```
[
    {
        "id": 1,
        "name": "foo",
        "parts": 5,
        "created": "2021-12-14 23:41:35",
        "updated": "2021-12-14 23:41:35"
    }
]
```
---
`POST` `/widget`

Accepts JSON payload of `name` and `parts`:
```
{
    "name": "foo",
    "parts": 5
}
```
Returns created object:
```
{
    "id": 1,
    "name": "foo",
    "parts": 5,
    "created": "2021-12-14 23:41:35",
    "updated": "2021-12-14 23:41:35"
}
```
---
`GET` `/widget/<id>`

Returns requested object:
```
{
    "id": 1,
    "name": "foo",
    "parts": 5,
    "created": "2021-12-14 23:41:35",
    "updated": "2021-12-14 23:41:35"
}
```
---
`PUT` `/widget/<id>`

Accepts JSON payload of `name` and `parts`:
```
{
    "name": "bar",
    "parts": 7
}
```
Returns updated object:
```
{
    "id": 1,
    "name": "bar",
    "parts": 7,
    "created": "2021-12-14 23:41:35",
    "updated": "2021-12-14 23:47:16"
}
```
---
`DELETE` `/widget/<id>`

Deletes object and returns `204`

## Errors

On error, the API will return an error payload explaining what went wrong, and an appropriate status code.
```
{
    "message": "Invalid request payload"
}
```
Some status codes and messages are:

 * `400`: "Invalid request payload"
 * `400`: "Invalid argument: name is greater than 64 characters"
 * `400`: "Missing argument 'name'"
 * `404`: "A Widget with id '{id}' was not found"
 * `409`: "A Widget with name '{name}' exists"
 * `500`: "Server Error"
