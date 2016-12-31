from library.domain import Dnsapi
from library import catchip
from time import sleep
import logging,sys
import logging.handlers

params = {
    "login_token":"你的API Token",
    "domain_id":"域名id",
    "record_id":"记录id(主机id)",
    "sub_domain":"主机名",#你的子域名 比如www.abc.com,则填"www"
    "record_line":"默认",#这里可以不用修改
    }

#from params import params
#日志初始化
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
if sys.platform.startswith("windows"):
    filename = "./dnspod.log"
else:
    filename = "/var/log/dnspod.log"
file_handler = logging.handlers.RotatingFileHandler(
                            filename=filename,
                            mode='a',
                            maxBytes=1024*1024
                            )
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

#安装log
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


def get_localip(i,logger=None):
    fun_dic = dict(
        taobao = catchip.getip_taobao,
        ip138 = catchip.getip_138,
        dnspod = catchip.getip_dnspod,
        )
    fun_list = ["dnspod","taobao","ip138"]
    while i <= 2:
        logger.debug("开始使用{} 获取ip".format(fun_list[i]))
        try:
            ip = fun_dic.get(fun_list[i])()
        except Exception as e:
            if logger:
                logger.exception("{} 获取ip失败，详情如下:".format(fun_list[i]) )
            i += 1
            continue
        else:
            return (ip,i)
    return (None,i%3)


if __name__ == "__main__":

    i = 0#本地ip查询
    min = 0#计时器60min一次循环
    sleep_time = 20#循环持续时间
    record = Dnsapi(**params)
    while True:
        local_ip,i = get_localip(i,logger)
        if local_ip is None:
            sleep(sleep_time) #休息60秒，进入下一轮循环
            logger.warning("本轮获取本地ip失败，进入下一轮")
            continue
        if min == 0:
            logger.info("每60分钟开始获取一次服务器ip")
            try:
                server_ip = record.get_ip()
            except Exception as e:
                logger.exception("获取服务器ip失败")
                sleep(sleep_time)
                continue
        if local_ip == server_ip:
            if min < 6:
                logger.info("本地ip:{}与服务器ip{}一致，无需更新".format(local_ip,server_ip))
            if min == 6:
                logger.info("过滤重复5次以上日志信息...")

        else:
            logger.info("本地ip{}与服务器ip{}不一致,开始更新".format(local_ip,server_ip))
            record.update_ip(local_ip)
            server_ip = local_ip
            min = 0
        min = (min+1) % 60
        sleep(sleep_time)
