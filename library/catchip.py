#获取ip的几种方式
import socket,re
import urllib.request
import json

#dnspod 比较简洁，但是经常不管用,留作备选
def getip_dnspod():
    sock = socket.create_connection(('ns1.dnspod.net', 6666),20)
    ip = sock.recv(16)
    sock.close()
    return ip.decode()

# 138ip
def getip_138(url="http://1212.ip138.com/ic.asp"):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    headers = {"User-Agent":user_agent}
    req = urllib.request.Request(url,headers = headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode("gbk")
    response.close()
    p = re.compile("((?:\d{1,3}\.){3}\d{1,3})")
    resault = p.search(data)
    if resault:
        ip = resault.group(0)
        return ip
    else:
        raise ValueError("没有匹配到ip")

#从淘宝获取ip
#http://ip.taobao.com/service/getIpInfo2.php?ip=myip 获取自己的ip
#http://ip.taobao.com//service/getIpInfo.php?ip=[ip]查询指定ip
def getip_taobao():
    url = "http://ip.taobao.com/service/getIpInfo2.php?ip=myip"
    data = urllib.request.urlopen(url).read().decode()
    ip = json.loads(data)['data']['ip']
    return ip


# dd_wrt路由器可以无密码显示wan_ip
def getip_ddwrt(url = "http://192.168.1.1"):
    #如果你的路由ip不是192.168.1.1，改成你需要的 ip = getip_ddwrt("http://你的ip")
    data = urllib.request.urlopen(url).read().decode()
    ip = re.findall("\"wan_ipaddr\">((?:\d{1,3}\.){1,3}\d{1,3})",data)[0]
    return ip

#其他路由器各不相同，只有各显神通了

#轮训测试
def loop_test():
    dic = {
    "taobao":getip_taobao,
    "ddwrt":getip_ddwrt,
    "138ip":getip_138,
    "dnspod":getip_dnspod,
    }
    for key in dic:
        try:
            print("%s 的解析结果为：%s" % (key,dic[key]()))
        except Exception as e:
            print("通过%s获取ip失败，原因为：%s" % (key,e))
