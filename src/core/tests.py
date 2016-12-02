from django.test import TestCase
import requests

# Create your tests here.
req = requests.get('http://www.baidu.com')
print(req.url)

