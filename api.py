import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '',
}

params = urllib.parse.urlencode({
    # 'players':'budbudhardy'
})

try:
    conn = http.client.HTTPSConnection('www.haloapi.com')
    conn.request("GET", "/stats/h5/servicerecords/custom?players=budbudhardy", "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
