import socket, ssl, os, json

class ServerConnection(object):

    def __init__(self, name, ip, port, key):
        self.name = name
        self.ip = (ip, port)
        self.key = key
    
    def getName(self):
        return self.name
    
    def getIp(self):
        return self.ip
    
    def getKey(self):
        return self.key
    
    def connect(self, *args):
        if not args:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(120)

        sslSock = ssl.wrap_socket(sock, ca_certs='ca.crt', cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2)

        args = [str(arg) for arg in args]
        args.insert(1, self.key)
        sslSock.connect(self.ip)
        sslSock.sendall('\n'.join(args) + '\n')
        
        fullData = []
        
        while True:
            data = sslSock.recv(32768)

            if data:
                if data.endswith('/x08'):
                    fullData.append(data[:-4])
                    break
                else:
                    fullData.append(data)

        fullData = ''.join(fullData)
        return json.loads(fullData)