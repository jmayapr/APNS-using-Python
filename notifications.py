import ssl
import json
import socket
import struct
import binascii


def send_push_message(token, payload):
    # the certificate file generated from Provisioning Portal
    certfile = 'pushcert.pem'
    #print(len(token))
    # APNS server address (use 'gateway.push.apple.com' for production server)
    apns_address = ('gateway.sandbox.push.apple.com', 2195)
 
    # create socket and connect to APNS server using SSL
    s = socket.socket()
    sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23 , certfile=certfile)
    sock.connect(apns_address)
 
    # generate APNS notification packet
    token = binascii.unhexlify(token)
    fmt = "!cH32sH{0:d}s".format(len(payload))
    cmd = '\x00'
    
    cmd = bytes(cmd, "utf-8")
    payload = bytes(payload, "utf-8")
    
    msg = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
    
    sock.write(msg)
    sock.close()
 
if __name__ == '__main__':
    payload = {"aps": {"alert": "Hellow World Push Notification","sound": "default"}
    send_push_message("800000a46dd7ef0c48ba7431868edefafb604e9eb33d5ef92fb38c5f83212", json.dumps(payload))