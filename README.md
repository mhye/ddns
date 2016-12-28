# ddns
Dynamic update dns by python

动态注册dnspod
## 本机ip的获取方式
1. dnspode提供的获取方式
2. 访问本机所在的路由器
3. 第三方网站taobao,ip138等

## 更新机制
获取本地ip，获取服务器ip，比对差异。如果相同则无需更新。如果不填则更新。第一次比对结束以后，本地缓存服务器ip，每分钟一次，比对新获取的ip与缓存服务器ip差异，相同无需更新，如果不同的话更新ip。
