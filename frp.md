# 下载
    github:
    git clone https://github.com/fatedier/frp.git

    gitlab:
    git clone http://gitlab.esuoyanyu.com/system/frp.git
## 配置文件
### frps.ini
    [common]                                                
    bind_port = 7000          #端口号                                       
    dashboard_port =          #管理页面端口号 
    dashboard_user =          #管理页面用户名 
    dashboard_pwd =           #管理页面密码
    token =                   #token client和server端要匹配 

    max_pool_count = 5        #最大连接数量 
    log_file =                #frps日志文件
    log_level = info          #日志级别 
    log_max_days = 3          #保存天数 
### frpc.ini
    [common]
    server_addr =             #frps的ip或域名
    server_port =             #frps的端口号 
    token =                   #token client和server要匹配

    [ssh]
    type = tcp                #使用的协议类型
    local_ip = 127.0.0.1      #本地ip
    local_port = 22           #本地服务使用的端口号
    remote_port =             #远程访问的端口号
    use_encryption = true
    use_compression = true

    [smb]
    type = tcp
    local_ip = 127.0.0.1
    local_port = 445
    remote_port =
    use_encryption = true
    use_compression = true

    [gitlab]
    type = http
    local_ip = 192.168.2.100
    local_port = 80
    custom_domains = gitlab.esuoyanyu.com

## 配置
### frps
    cp frps /etc/init.d
    cp frps.server /lib/systemd/system
    ln -s /lib/systemd/system/frps.server /etc/systemd/system/multi-user.target.wants/frps.server
### frpc
    cp frpc /etc/init.d
    cp frpc.server /lib/systemd/system
    ln -s /lib/systemd/system/frpc.server /etc/systemd/system/multi-user.target.wants/frpc.server

## frps-plugin
### 配置文件
```
    [plugin.frps.position]
    addr = 10.0.0.4:8090
    path = /handler
    ops = Login,NewWorkConn,NewUserConn
```

### 配置
```
chmod +x ./frps-position.py
sudo cp ./frps-position /etc/init.d/
sudo chmod +x /etc/init.d/frps-position
sudo cp ./frps-position.service /lib/systemd/system
sudo ln -s /lib/systemd/system/frps-position.service /etc/systemd/system/multi-user.target.wants
```

## 通知
### 安装
```
sudo apt install mailutils
sudo apt install ssmtp
```
### 配置
```
sudo vim /etc/ssmtp/revaliases
chy:esuoyanyu_notify@126.com:smtp.126.com:465

sudo vim /etc/ssmtp/ssmtp.conf
root=postmaster
mailhub=smtp.126.com:465
hostname=localhost.localdomain
AuthUser=esuoyanyu_notify@126.com
AuthPass=
UseTLS=YES

```