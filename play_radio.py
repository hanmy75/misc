#!/usr/bin/python3

import requests, re, json
import subprocess, sys
import os, signal


def check_kill_process(pstring):
    for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        os.kill(int(pid), signal.SIGKILL)

def url_func(url):
    resp = requests.get(url)
    data = resp.content.decode("utf-8")
    return data

def kbs_func(code):
    Base_URL = 'http://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=' + code
    WebHTML = url_func(Base_URL)
    Temp_Web_URL = re.compile('http://.*_lsu_sa_=[0-9a-z]*').findall(WebHTML)
    url = Temp_Web_URL[0].split('\\', 1)[0]
    ### Double query
    #url_root = url.rsplit('/', 1)[0]
    #M3U = url_func(url)
    #M3U = re.compile('.*m3u.*').findall(M3U)[0]
    #url = url_root + '/' + M3U
    ###
    return url

def mbc_func(code):
    Base_URL = 'http://miniplay.imbc.com/AACLiveURL.ashx?channel=' + code + '&type=iphone&agent=iphone&protocol=M3U8'
    url = url_func(Base_URL)
    ### Double query
    #url_root = url.rsplit('/', 1)[0]
    #M3U = url_func(url)
    #M3U = re.compile('.*m3u.*').findall(M3U)[0]
    #url = url_root + '/' + M3U
    ###
    return url

def sbs_func(code):
    Base_URL = 'http://apis.sbs.co.kr/play-api/1.0/onair/channel/' + code + '?v_type=2&platform=pcweb&protocol=hls&ssl=N&jwt-token=&rnd=101'
    data = json.loads(url_func(Base_URL))
    url = data.get('onair').get('source').get('mediasource').get('mediaurl')
    ### Double query
    #print(url)
    #M3U = url_func(url)
    #url = re.compile('.*m3u.*').findall(M3U)[0]
    ###
    return url

def ch_func(ch):
    if   ch == "KBS 1FM":
        url = kbs_func('24')
    elif ch == "KBS 2FM":
        url = kbs_func('25')
    elif ch == "KBS 1R":
        url = kbs_func('21')
    elif ch == "KBS 2R":
        url = kbs_func('22')
    elif ch == "KBS 3R":
        url = kbs_func('23')
    elif ch == "MBC FM4U":
        url = mbc_func('mfm')
    elif ch == "MBC FM":
        url = mbc_func('sfm')
    elif ch == "SBS Power FM":
        url = sbs_func('S07')
    elif ch == "SBS Love FM":
        url = sbs_func('S08')
    else:
        print("Argument(%s) is missing or invalid!" % ch)
        quit()
    return url

def play_func(url):
    FFMPEG_CMD = "ffmpeg -i {}{}{} -f alsa default 2>/dev/null &".format("\'", url, "\'")
    subprocess.call(FFMPEG_CMD, shell=True)

def run_mkchromecast(device):
    CAST_CMD = "mkchromecast -n {}{}{} 2>/dev/null &".format("\'" ,device, "\'")
    subprocess.call(CAST_CMD, shell=True)

def run_pulseaudio():
    PULSEAUDIO_CMD = "pulseaudio -D"
    subprocess.call(PULSEAUDIO_CMD, shell=True)

# Main
# Kill ffmpeg & mkchromecast is it is already running
check_kill_process('pulseaudio')
check_kill_process('mkchromecast')
check_kill_process('ffmpeg')

# Run mkchromecast
run_pulseaudio()
run_mkchromecast("MY Mini")

# Get Radio URL
url = ch_func(sys.argv[1])

# Play URL
play_func(url)
