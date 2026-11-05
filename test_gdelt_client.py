import io, unittest
from unittest.mock import patch
import gdelt_client

class Response:
    headers={"Content-Type":"application/json"}
    def __init__(self, body):self.body=body
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self,*args):return self.body

class GdeltTests(unittest.TestCase):
    @patch('gdelt_client._pace')
    @patch('gdelt_client.urllib.request.urlopen')
    def test_normal_json(self, opener, pace):
        opener.return_value=Response(b'{"articles":[{"title":"Test"}]}')
        self.assertEqual(gdelt_client.fetch_articles('test'), [{'title':'Test'}])

    @patch('gdelt_client._pace')
    @patch('gdelt_client.urllib.request.urlopen')
    def test_invalid_html_detected(self, opener, pace):
        opener.return_value=Response(b'<html>Error</html>')
        with self.assertRaises(gdelt_client.GDELTError) as ctx:
            gdelt_client.fetch_articles('test')
        self.assertEqual(ctx.exception.code, 'invalid_response')

if __name__ == '__main__':unittest.main()
