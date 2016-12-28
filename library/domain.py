#以下参考官方样例https://github.com/DNSPod/dnspod-python/blob/master/dnspod/apicn.py
import urllib
import urllib.request
import json

class domain:
    def __init__(self,login_token,domain_id,email,**kw):
        #初始化login_token和Domain,lgin_token为"id,token"
        #参见https://support.dnspod.cn/Kb/showarticle/tsid/227/
        self.baseurl = "https://dnsapi.cn/"
        self.email = email

        #公共参数
        self.params =dict(
        login_token = login_token,
        domain_id = domain_id,
        format = 'json'
        )
        self.params.update(kw)
    def request(self,sub_url,**kw):
        url = self.baseurl+sub_url
        #开发规范要求头部文件不能模拟浏览器，然后必须包含邮箱不知道什么意思，试过模拟浏览器好像没有发生过什么问题
        headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/json",
         "User-Agent": "my_python_client/0.01 (%s)" % self.email
         }
        params = self.params
        params.update(kw)

        data = urllib.parse.urlencode(params).encode('utf-8')
        req = urllib.request.Request(url,data,headers)
        response = urllib.request.urlopen(req).read().decode()

        resault = json.loads(response)

        if resault.get("status").get("code")=="1":
            return resault
        else:
            raise Exception(resault)
    ```
    可以试试通过这些资料获取一些信息，比如
    dm = domian(xxxx)
    #获取域名日志
    dm.request("Domain.Log")
    #获取域名信息
    dm.request("Domain.Info")
    #获取子域名列表
    dm.request("Record.List")
    然后子域名里你也可以找到你感兴趣的兴趣，比如record
    ```
