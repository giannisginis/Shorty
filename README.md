# <img src="documents/icons/logo.jpeg" width="250" height="150"/>&nbsp;&nbsp;&nbsp;

# Shorty

A Url shortener API.


## Table of Contents

* [Overview](#overview)
* [Design](#design)
* [Installation](#installation)
* [Execution](#execution)

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

### Technology stack

* [Python 3.7.x](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Pytest](https://docs.pytest.org/en/stable/)
* [Pytest-mock](https://github.com/pytest-dev/pytest-mock/)

## Design

The `Shorty` architecture and design are given in detail in the [design documentation](documents/design.md). 


## Installation

Installation guidelines can be found in [the installation document](documents/installation.md).


## Execution

Activate virtual environment:
```Python
$ source path2venv/bin/activate
```
Clone the project:
```bash
$ git clone https://github.com/giannisginis/Shorty.git
```
CD to project:
```bash
$ cd Shorty
```

Start flask server locally:

```Python
$ python run.py
```
Or if you prefer Start flask server with `docker` (docker is required):

```Bash
$ docker build -t shorty:latest .
$ docker run -p 5000:5000 -d shorty
```
Make the request:

```bash
$ curl -i -H "Content-Type: application/json" -X post -d '{"url":"https://www.example.com", "provider": "tinyurl"}' http://127.0.0.1:5000/shortlinks
```
