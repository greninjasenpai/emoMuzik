import http.client, urllib.request, urllib.parse, urllib.error, base64


headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '4c8334d694de4146a748230788ad2f49',
}

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,emotion',
})

body = "" 

#load image

filename = 'happy.jpeg'

f = open(filename, "rb")

body = f.read()

print(body)

f.close()

try:
    conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

# from PIL import Image 

# def main(): 
#     try: 
#         #Relative Path 
#         img = Image.open("picture.jpg") 
        
#         #Angle given 
#         img = img.rotate(180) 
        
#         #Saved in the same relative location 
#         img.save("rotated_picture.jpg") 
#     except IOError: 
#         pass

# if __name__ == "__main__": 
#     main()

