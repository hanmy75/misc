import requests

#URL = "http://miniplay.imbc.com/AACLiveURL.ashx?protocol=RTMP&channel=mfm"
#URL = "http://miniplay.imbc.com/AACLiveURL.ashx?protocol=M3U8&channel=mfm&agent=android&androidVersion=24"
URL = "http://miniplay.imbc.com/AACLiveUrl.ashx?channel=mfm&type=iphone&agent=iphone&protocol=M3U8"

# Main
resp = requests.get(URL)
data = resp.content.decode("utf-8")
print(data)
