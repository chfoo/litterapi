=========
Litterapi
=========

An API built from Twitter's web interface.

Twitter's API doesn't serve the same results from their web search especially with historical operators. This Python library exposes an API scraped from their web pages.

Search is currently supported.


Install
=======

Requires:

* Python 3.2 or greater
* requests
* html5lib

If you have pip, you can run::

    pip3 install git+https://github.com/chfoo/litterapi#egg=litterapi --user


Quick Start
===========

To start searching quickly::

    python3 -m litterapi search "cat"


Will return JSON formatted lines (line-breaks added for clarity)::

    {
        "tweet_id": "12345",
        "screen_name": "catlover456",
        "user_id": "7890",
        "timestamp": 14567890,
        "text": "Have you seen this cat? So cute! pic.twitter.com/photo/abcd,
        "urls": [
            ["http://t.co/abcdef134", "http://pic.twitter.com/photo/abcd"]
        ]
    }


Through the fake API::

    api = SearchAPI('cat')

    while True:
        results = api.fetch()

        if not results:
            break

        for result in results:
            print(json.dumps(result))

        time.sleep(1)

