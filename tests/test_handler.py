import unittest
import index
from testevent import eventobj

class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("testing response.")
        print(eventobj)
        result = index.lambda_handler(eventobj,{})
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('{"Credit-cards"', result['body'])


if __name__ == '__main__':
    unittest.main()
