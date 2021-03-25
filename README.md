# Shorty

A Url shortener API.


## Table of Contents

* [Overview](#overview)
* [Design](#design)
* [Installation](#installation)
* [Execution](#execution)
* [Interface](#interface)
* [Deployment](#-deployment)
* [Configuration](#-configuration)
* [Contributing](#-contributing)
* [Changelog](#-changelog)

Software Engineer Task
======================

At Plum, we have a lot of services that need to work together to deliver our product.
Many of these services talk to third-party providers to perform their operations – for
example moving money, performing background checks, sending messages or emails, etc.

In a lot of cases - due to business, compliance or technical reasons - we need to support
multiple third-party providers for the same operation, some of which have wildy different
specifications, ranging from simple REST APIs to SOAP.

To maintain our sanity, we abstract these third-parties behind interfaces and expose
consistent APIs for the rest of the system to consume. Each service should be able to
pick sensible defaults (and fallbacks, if, for example, a provider is unavailable) or
allow the consumer to specify the provider if they wish to do so.

Overview
-------

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

The `ml-server` architecture and design are given in detail in the [design documentation](docs/design.md). 


## Installation

Installation guidelines can be found in [the installation document](docs/installation.md).


## Execution

With the virtual enviroment installed:
Start flask server running:

```Python
python run.py
```
make the request:

```bash
curl -i -H "Content-Type: application/json" -X get -d '{"url":"www.example.com", "provider": "tinyurl"}' http://127.0.0.1:5000/shortlinks
```

Deliverable
-----------

You should deliver your solution as a Pull Request in your repo. Document your design choices and anything else you think we need to know in the PR description.

What we look for
----------------

In a nutshell, we're looking for tidy, production-quality code, a scalable design and sensible
tests (unit tests, integration tests or both?). Imagine that your code will be read by other 
developers in your team – keep them happy :-)

Resources
---------

1. `Flask`: http://flask.pocoo.org/
2. `pytest`: http://pytest.org/latest/
3. `virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/latest/
4. `HTTP statuses`: https://httpstatuses.com/

Disclaimer
----------

We will not use any of this code for any of Plum's applications.
