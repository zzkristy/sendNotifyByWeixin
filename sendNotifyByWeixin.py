#!/usr/bin/env python3
# coding:utf-8
# 使用微信客服消息接口给用户发消息

try:
    import urllib2
    import urllib
    urlencode = urllib.urlencode
except:
    import urllib.request as urllib2
    import urllib
    urlencode = urllib.parse.urlencode

import json
import pickle
import datetime
import time

appid = 'wxe69eb70c8b3f3a5b'
secret = '36a3de6f1c0012cc7bf85abc3929f409'
openid_list = ["oEBI5s6K22zpOidPFA-ts74-LLOs"]
data_pkl = 'token_data.pkl'


def url_request(url, values={}, method='GET'):
    if method == 'GET':
        if len(values) != 0:
            url_values = urlencode(values)
            furl = url + '?' + url_values
        else:
            furl = url
        req = urllib2.Request(furl)
    elif method == 'POST':
        data = json.dumps(values, ensure_ascii=False)
        req = urllib2.Request(url, data.encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        req.get_method = lambda: 'POST'
    else:
        pass

    try:
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')
        response = urllib2.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(str(e))
        result = {}
    return result


def get_token():
    try:
        f = open(data_pkl, 'rb')
        data_dict = pickle.load(f)
        f.close()
    except:
        data_dict = {}
    try:
        expires_time = data_dict['expires_time']
        access_token = data_dict['access_token']
    except:
        expires_time = 0
        access_token = ''

    now_time = int(time.mktime(datetime.datetime.now().timetuple()))
    if now_time >= expires_time:
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        values = {
            'appid': appid,
            'secret': secret,
            'grant_type': 'client_credential'
        }
        result = url_request(url, values, method='GET')
        if len(result) != 0:
            now_time = int(time.mktime(datetime.datetime.now().timetuple()))
            expires_time = now_time + 7200 - 10
            result['expires_time'] = expires_time
            f = open(data_pkl, 'wb')
            pickle.dump(result, f)
            f.close()
            access_token = result['access_token']
        else:
            access_token = ''
    else:
        access_token = data_dict['access_token']

    return access_token


def send_text_message(content):
    token = get_token()
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + token
    values = {
        'touser': 'oEBI5s6K22zpOidPFA-ts74-LLOs',
        "msgtype": "text",
        "text": {
            "content": content
        },
    }
    result = url_request(url, values, method='POST')
    print(result)
    return result


def main():
    send_text_message('world')

if __name__ == "__main__":
    main()
