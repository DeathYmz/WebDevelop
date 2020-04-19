需要条件：
mysql
工具中安装：
pymysql;flask;qrcode
(1)运行本项目 只需要打开/app/config.py 修改参数（ip为本机无线局域网适配器 WLAN:的地址。sqlname和sqlpasswar 为登录mysql的账户和密码 sqldatabase 为数据库库名）
(2) 运行mod_db 中的/app/mod_db/createtable.py 创建本项目需要的表
(3) 运行/app/blockchainServer.py 
之后便可输入地址 http://ip:5000/login (ip 与上相同)
