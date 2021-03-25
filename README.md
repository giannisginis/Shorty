# Shorty

A Url shortener API.


## Table of Contents

* [Overview](#overview)
* [Design](#design)
* [Installation](#installation)
* [Execution](#execution)
* [Interface](#interface)

Overview
---------

`Shorty` is a microservice which supports two URL shortening providers: [bit.ly](https://dev.bitly.com/) and [tinyurl.com](https://gist.github.com/MikeRogers0/2907534). The service exposes a single endpoint: `POST /shortlinks`. The endpoint receive
JSON with the following schema:

| param    | type   | required | description                        |
|----------|--------|----------|------------------------------------|
| url      | string | Y        | The URL to shorten                 |
| provider | string | N        | The provider to use for shortening |

The response is a `Shortlink` resource containing:

| param    | type   | required | description                        |
|----------|--------|----------|------------------------------------|
| url      | string | Y        | The original URL                   |
| link     | string | Y        | The shortened link                 |

For example:
```json
{
    "url": "https://example.com",
    "link": "https://bit.ly/8h1bka"
}
```

If the provider is not supplied the microservice by default uses `bit.ly` and in case is not available fallback to `tinyurl`.

### Technology stack

* [Python 3.7.x](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Pytest](https://docs.pytest.org/en/stable/)
* [Pytest-mock](https://github.com/pytest-dev/pytest-mock/)

## Design

The `Shorty` architecture and design are given in detail in the [design documentation](documentss/design.md). 


## Installation

Installation guidelines can be found in [the installation document](documentss/installation.md).


## Execution

Activate virtual environment:
```Python
$ source path2venv/bin/activate
```

Start flask server running:

```Python
$ python run.py
```
make the request:

```bash
$ curl -i -H "Content-Type: application/json" -X get -d '{"url":"www.example.com", "provider": "tinyurl"}' http://127.0.0.1:5000/shortlinks
```

Resources
---------

1. `Flask`: http://flask.pocoo.org/
2. `pytest`: http://pytest.org/latest/
3. `virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/latest/
4. `HTTP statuses`: https://httpstatuses.com/
