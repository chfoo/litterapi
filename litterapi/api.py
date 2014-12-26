import abc
import urllib.parse
import html5lib

import requests


class BaseAPI(object, metaclass=abc.ABCMeta):
    def __init__(self, timeout=60):
        super().__init__()
        self._timeout = timeout

    @abc.abstractmethod
    def fetch(self):
        pass

    def _make_request(self, url):
        return requests.get(url, timeout=self._timeout)


class SearchAPI(BaseAPI):
    URL = ('https://twitter.com/i/search/timeline?f=realtime&q={query}'
           '&src=typd&include_available_features=1&include_entities=1')

    def __init__(self, query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._query = query
        self._cursor = None

    def fetch(self):
        url = self.URL.format(query=urllib.parse.quote_plus(self._query))

        if self._cursor:
            url += '&scroll_cursor={}'.format(self._cursor)

        response = self._make_request(url)

        doc = response.json()
        self._cursor = doc.get('scroll_cursor')

        html_content = doc['items_html']
        results = tuple(self._scrape_html(html_content))

        return results

    def _scrape_html(self, content):
        document = html5lib.parse(content)

        for tweet_element in document.findall(
                './/{http://www.w3.org/1999/xhtml}div[@data-tweet-id]'):
            tweet_id = tweet_element.get('data-tweet-id')
            screen_name = tweet_element.get('data-screen-name')
            user_id = tweet_element.get('data-user-id')

            timestamp_element = tweet_element.find(
                './/{http://www.w3.org/1999/xhtml}span[@data-time]')
            timestamp = int(timestamp_element.get('data-time'))

            content_element = tweet_element.find(
                ".//{http://www.w3.org/1999/xhtml}p")

            text_list = []

            def walk(element):
                if element.get('class') == 'tco-ellipsis':
                    return

                text_list.append(element.text or '')
                for sub_element in element:
                    walk(sub_element)

                if element != content_element:
                    text_list.append(element.tail or '')

            walk(content_element)

            text = ''.join(text_list)
            urls = []

            for link_element in content_element.findall(
                    './/{http://www.w3.org/1999/xhtml}a[@href]'):
                urls.append(
                    (link_element.get('href'),
                     link_element.get('data-expanded-url')
                    )
                )

            yield {
                'tweet_id': tweet_id,
                'screen_name': screen_name,
                'user_id': user_id,
                'timestamp': timestamp,
                'text': text,
                'urls': urls,
            }
