import requests
import json
request = requests.get(url="http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=440&count=3&maxlength=300&format=json").json()
print(request)
