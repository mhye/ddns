#参数

params = {
    "login_token":"你的API Token",
    "domain_id":"域名id",
    "record_id":"记录id(主机id)",
    "sub_domain":"主机名",#你的子域名 比如www.abc.com,则填"www"
    "record_line":"默认",#这里可以不用修改
    }

from library.domain import Dnsapi
from library import catchip
from time import sleep

def get_localip(i):
    fun_dic = dict(
        taobao = catchip.getip_taobao,
        ip138 = catchip.getip_138,
        dnspod = catchip.getip_dnspod,
        )
    fun_list = ["dnspod","taobao","ip138"]
    while i <= 2:
        try:
            ip = fun_dic.get(fun_list[i])()
        except Exception as e:
            print(e)
            i += 1
            continue
        else:
            return (ip,i)
    return (None,i%3)


if __name__ == "__main__":

    i = 0
    min = 0
    sleep_time = 20
    record = Dnsapi(**params)
    server_ip = record.get_ip()
    while True:
        local_ip,i = get_localip(i)
        if local_ip is None:
            sleep(sleep_time) #休息60秒，进入下一轮循环
            continue
        if min = 59:
            try:
                server_ip = record.get_ip()
            except Exception as e:
                print(e)
                sleep(sleep_time)
                continue
        print("本地ip：%s，服务器ip：%s" %(local_ip,server_ip))
        if local_ip == server_ip:
            print("本地ip与服务器一致，无需更新")
        else:
            print("本地服务器与服务器ip不一致")
            record.update_ip(local_ip)
            serer_ip = local_ip
        i = (i+1) % 60
        sleep(sleep_time)
