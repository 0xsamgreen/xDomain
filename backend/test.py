import requests
import json

url = 'http://localhost:8000/data_daily_opp'
print(requests.get(url).json())