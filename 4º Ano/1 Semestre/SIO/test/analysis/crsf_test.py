

# importing the requests library
import requests
 
# api-endpoint
URL = "http://127.0.0.1:5000/"
 

 
# sending get request and saving the response as response object
url = URL + "auth/login"
data = {'username':'admin', 'password':'admin'}
r = requests.post(url = url, data = data)

print(r.text)