
import urllib.request
import json

def seurityEncode(password):
    '''
    首先，mercury的密码加密方式
    下面的函数是翻译了Mercury里js脚本制作出来的
    这个函数是参照Mercury路由器的js脚本写的，拿到手的几个路由器的start参数和字典都是一样的
    似乎并没有别的机制初始化starDe和dic
    '''
    output = ""
    start = "RDpbLfCPsJZ7fiv"
    dic = ("yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciX"
           "TysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgML"
           "wygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3"
           "sfQ1xtXcPcf1aT303wAQhv66qzW")

    lens = max(len(start),len(password))
    for i in range(lens):
        cl = 0xBB
        cr = 0xBB
        if i >= len(start):
            cr = ord(password[i])
        elif i >= len(password):
            cl = ord(start[i])
        else:
            cl = ord(start[i])
            cr = ord(password[i])
        output += dic[(cl^cr)%len(dic)]
    return output


#读取内容的函数
def get_data(url,data=None):
    headers = {#"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
              #"Referer": "http://192.168.4.1/",
              #"Accept": "application/json, text/javascript, */*; q=0.01",
              #"X-Requested-With": "XMLHttpRequest",
              #"Content-Type": "application/json; charset=UTF-8"
              }
#水星的路由器对请求头验证不是很严格，我把这些都关闭了似乎也一切正常，如果你们有需要自己关闭注释
    data = json.dumps(data).encode("utf-8")
    #data = urllib.parse.urlencode(data)
    #data = data.encode("utf-8")
    req = urllib.request.Request(url,data,headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    response.close()
    return data

def get_wanip(url,password):
    '''
    这个函数演示了如何通过密码获取wan_ip
    用法示例：get_wanip("http://192.168.1.1","123456")
    不过速度应该比不上socket dnspod,好处是你家路由器不会拒绝你
    '''
    params ={"method":"do","login":{"password":seurityEncode(password)}}
    #首先获取动态链接
    data = get_data(url,params).decode()
    stok = json.loads(data).get("stok")

    #url
    url = url+"stok="+stok+"/ds"
    #请求参数
    #print(url)
    params2 = {"protocol":{"name":["pppoe","wan"]},"network":{"name":"wan_status"},"method":"get"}
    data = get_data(url,params2)
    ip =json.loads(data.decode()).get("network").get("wan_status").get("ipaddr")
    return ip
