import requests
api_url = "https://api.weatherapi.com/v1/current.json?key=&q=Jamaica&aqi=no"

response = requests.get(api_url)

print( response.json())