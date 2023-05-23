#!/usr/bin/env python

# coding=< UTF-8>

import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

import log
 
host = ('10.0.0.4', 8090)
#host = ('127.0.0.1', 8090)

def get_position_ip_api(req_posi):
    url = 'http://ip-api.com/json/' + req_posi
    res = requests.get(url)
    resp = json.loads(res.text)
    status = resp['status']
    #print(resp)
    if status == 'success':
        return resp['country']
    else:
        return 'No Find'

def get_position_freeapi(req_posi):
    url = 'http://freeapi.ipip.net/' + req_posi
    res = requests.get(url)
    resp = res.json()
    #print(resp[0])

    return resp[0]

class Resquest(BaseHTTPRequestHandler):
    timeout = 5
    server_version = "Apache" 

    def do_POST(self):
        path = self.path
        idx0 = path.find('/')
        idx1 = path.find('?')
        path = path[idx0 + 1 : idx1]
        print(path)
        if path != 'handler':
            self.send_response(400)
            self.end_headers()
            return False
        req_data = self.rfile.read(int(self.headers['content-length']))
        req_json = json.loads(req_data)
        op = req_json['op']
        content = req_json['content']
        if op == 'Login':
            proxy_name = 'login'
            client_address_port = content['client_address']
        elif op == 'NewUserConn':
            proxy_name = content['proxy_name']
            client_address_port = content['remote_addr']

        if op == 'Login' or op == 'NewUserConn':
            idx = client_address_port.find(":")
            if idx > 0 and idx < len(client_address_port):
                    client_address = client_address_port[:idx]
            else:
                    logger(log.error, "{} address invalid\n".format(client_address_port))
                    return False
        elif op == 'Ping':
            self.send_response(200)
            self.end_headers()
            rep = '{"reject": false, "unchange": true}'
            self.wfile.write(rep.encode())
            return True
        else:
            logger.write(log.ERROR, "op={} not support\n".format(op))
            self.send_response(403)
            self.end_headers()
            return True

        status = get_position_ip_api(client_address)
        if status == 'China':
            allow = True
        elif status == 'No Find':
            status = get_position_freeapi(client_address)
            if status == '中国':
                allow = True
            else:
                allow = False
        else:
            allow = False
        ack = {}        
        if allow == True:
            ack['reject'] = False
            ack['unchange'] = True
            logger.write(log.INFO, "op={}\ntype={}\nip={}\ncountry={}\nallow=true\n".format(op, proxy_name, client_address, status))
        else:
            ack['reject'] = True
            ack['reject_reason'] = 'invalid user'
            logger.write(log.ERROR, "op={}\ntype={}\nip={}\ncountry={}\nallow=false\n".format(op, proxy_name, client_address, status))

        str_ack = json.dumps(ack)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str_ack.encode())

        return True

logger = log.init_log()

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.write(log.ERROR, "main thread exit\n")
        exit(3)
    
