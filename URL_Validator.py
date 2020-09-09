import urllib.error
import urllib.request


def test_url(url):
    try:
        conn = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        # ...
        return f'HTTPError: {e.code}   {url}'
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        return f'URLError: {e.reason}   {url}'
    else:
        # 200
        # ...
        return 'Good'
