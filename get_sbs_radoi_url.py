#import urllib.request
#import urllib.parse
import requests

#URL = "http://apis.sbs.co.kr/play-api/1.0/onair/channel/S07?v_type=2&platform=pcweb&protocol=hls&ssl=N&jwt-token=&rnd=101"
URL = "http://apis.sbs.co.kr/play-api/1.0/onair/channel/S08?v_type=2&platform=pcweb&protocol=hls&ssl=N&jwt-token=&rnd=101"

#f = urllib.request.urlopen(URL)
#print(f.read().decode('utf-8'))


r = requests.get(URL)
data = r.json()
media_url = data.get('onair').get('source').get('mediasource').get('mediaurl')
if media_url != None:
    print("Media URL : " , media_url)
