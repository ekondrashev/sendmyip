'''
Created on May 14, 2015

'''
import socket
import fcntl
import struct
# import argparse


__author__ = "Eugene Kondrashev"
__copyright__ = "Copyright 2015, Eugene Kondrashev"
__credits__ = ["Eugene Kondrashev"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Eugene Kondrashev"
__email__ = "eugene.kondrashev@gmail.com"
__status__ = "Prototype"

# parser = argparse.ArgumentParser()
# parser.add_argument("user")
# parser.add_argument("pass")
# parser.add_argument("to")


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
    
    
def send(username, password, tousr, subj, body):
    headers = "\r\n".join(["from: " + username,
                       "subject: " + subj,
                       "to: " + tousr,
                       "mime-version: 1.0",
                       "content-type: text/html"])

    # body_of_email can be plaintext or html!                    
    content = headers + "\r\n\r\n" + body
    import smtplib

    # The below code never changes, though obviously those variables need values.
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(username, password)
    session.sendmail(username, tousr, content)

def main():
    ip = get_ip_address("eth0")
    send("user", "pass", "recipient", "New ip", ip)

if __name__ == "__main__":
    main()
    
    