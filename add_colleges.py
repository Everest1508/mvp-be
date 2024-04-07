import requests

url = 'https://apimvp.pythonanywhere.com/event/college/'
myobj = {'somekey': 'somevalue'}

x = requests.get(url)

print(x.text)