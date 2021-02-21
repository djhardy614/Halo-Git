import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

f = open('C:/Users/Public/Documents/key.txt', 'r')
key = f.read()
f.close()

headers = {
    # Request headers
    'Accept-Language': 'en',
    'Ocp-Apim-Subscription-Key': key,
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('www.haloapi.com')
    conn.request("GET", "/metadata/h5/metadata/maps?", "{body}", headers)
    response = conn.getresponse()
    my_bytes_value = response.read()
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

my_json = r(my_bytes_value.decode('utf8').replace("'", '"'))

data = json.loads(my_json)
s = json.dumps(data, indent=4, sort_keys=True)
print(s)