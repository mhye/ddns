from library.domain import Dnsapi
from library import catchip
import dump_params
from time import sleep
import logging,sys
import logging.handlers

para = {
    "login_token":"你的API Token",
    "domain_name":"域名",#你的域名 例如：abc.com
    "sub_domain":"主机名",#你的子域名 比如www.abc.com,则填"www"
    }
#from params import  para

#logger初始化
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
#windows平台在当前目录创建dnspod.log，linux平台在/var/log/dndpod.log
if sys.platform.startswith("windows"):
    filename = "./dnspod.log"
else:
    filename = "/var/log/dnspod.log"
file_handler = logging.handlers.RotatingFileHandler(
                            filename=filename,
                            mode='a',
                            maxBytes=1024*1024,
                            backupCount = 10,
                            )
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

#安装log
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


def get_localip(logger=None):
    fun_dic = dict(
        taobao = catchip.getip_taobao,
        ip138 = catchip.getip_138,
        dnspod = catchip.getip_dnspod,
        )
    fun_list = ["dnspod","taobao","ip138"]
    for item in fun_list:
        logger.debug("开始使用{} 获取ip".format(item))
        try:
            ip = fun_dic.get(item)()
        except Exception as e:
            if logger:
                logger.exception("通过{} 获取ip失败，详情如下:".format(item) )
            continue
        else:
            return (ip)
    return None


if __name__ == "__main__":

    min = 0#计时器60min一次循环
    sleep_time = 60#循环持续时间

    #初次循环，获取record_id以及相关信息。
    while True:
        try:
            data = dump_params.get_para(**para)
        except Exception as e:
            logger.warning("getting domain name base information failure,please check your network or para!")
            sleep(10)
            continue
        else:
            break

    record = Dnsapi(**data)
    #开始主循环
    while True:
        local_ip = get_localip(logger)
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
            if min < 5:
                logger.info("本地ip:{}与服务器ip{}一致，无需更新".format(local_ip,server_ip))
            if min == 5:
                logger.info("过滤重复5次以上日志信息...")

        else:
            logger.info("本地ip:{} 与服务器ip {}不一致,开始更新".format(local_ip,server_ip))
            try:
                resault = record.update_ip(local_ip)
            except Exception:
                logger.exception("更新ip失败：")
                min = 0
                continue
            logger.info("更新ip成功:\n{}".format(resault))
            server_ip = local_ip
            min = 0
        min = (min+1) % 60
        sleep(sleep_time)
