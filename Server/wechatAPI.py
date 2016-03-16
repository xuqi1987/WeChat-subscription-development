
# -*- coding:utf8 -*-
import requests
import json
import hashlib

class WechatAPI():
    def __init__(self):
        self.appid = 'wxe589b00c17795e10'
        self.secret = '577a346208002399faf26896e6462f12'
        # 获取access token
        self.token = ''
        self.expires = 0

        pass

    def wechat_auth(self,request):
        token = 'xq123456' # your token
        query = request.args  # GET 方法附上的参数
        signature = query.get('signature', '')  # 微信加密签名
        timestamp = query.get('timestamp', '')  # 时间戳
        nonce = query.get('nonce', '')  # 随机数
        echostr = query.get('echostr', '') # 随机字符串
        s = [timestamp, nonce, token]
        # 1. 将token、timestamp、nonce三个参数进行字典序排序
        s.sort()
        # 2. 将三个参数字符串拼接成一个字符串进行sha1加密
        s = ''.join(s)
        # 3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
        key = hashlib.sha1(s).hexdigest()
        if (key == signature):
            print "验证成功"
            return echostr
        raise Exception("验证失败")


    def get_token(self):
        # 因为有调用限制,所以不要每次都取
        params = {'grant_type':'client_credential',
                  'appid':'wxe589b00c17795e10',
                  'secret':'577a346208002399faf26896e6462f12'}
        url = "https://api.weixin.qq.com/cgi-bin/token"

        if self.token != '':
            resp = self.get(url,params)
            self.token = resp['access_token']
            self.expires = resp['expires_in']
            print resp
        pass

    def check_error(ret,self):
        if ret.has_key('errcode'):
            raise Exception(ret)


    def get(self,url,params):
        r = requests.get(url,params=params)
        print r.url
        print r.text
        ret = json.loads(r.text)
        self.check_error(ret)
        return ret