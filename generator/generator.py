import os
import random
import shutil
import string
import threading
import time
# import uuid
import SimpleHTTPServer,BaseHTTPServer
__author__ = 'eri'

log_patern = """
[32;01m[2013-06-19 12:21:37.194][000][10.23.11.190:47209]: EDGE: _on_recv_ok: ref_id:11[0m
[33;01m[2013-06-19 12:21:38.028][001][10.23.11.190:47210]: EDGE: _send_signalling_packet: type:8, ref_id:11[0m
[33;01m[2013-06-19 12:21:38.029][001][10.23.11.190:47210]: EDGE: _on_recv_ok: ref_id:11[0m
[33;01m[2013-06-19 12:21:38.029][001][10.23.11.190:47210]: EDGE: disconnect[0m
[%s][001]: ConnectTime=0.002 DoneTime=%2.3f DONE, session_start:0.005, max_ping1:0.001, stream_start:0.126, stream_end:0.262, max_ping2:0.001
[31;06m[2013-06-19 12:21:38.031][002][10.23.11.190:47214]: EDGE: connected[0m
[31;01m[2013-06-19 12:21:38.032][002][10.23.11.190:47214]: EDGE: _send_signalling_packet: type:0, ref_id:0[0m
[31;01m[2013-06-19 12:21:38.036][002][10.23.11.190:47214]: EDGE: _on_recv_ok: ref_id:0[0m
[32;01m[2013-06-19 12:21:38.196][000][10.23.11.190:47209]: EDGE: _send_signalling_packet: type:8, ref_id:12[0m
[32;01m[2013-06-19 12:21:38.197][000][10.23.11.190:47209]: EDGE: _on_recv_ok: ref_id:12
"""

def id_generator(size=32, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

class Loger(threading.Thread):

    def __init__(self, filename='./log',*args,**kwargs):
        self.fname = os.path.abspath(filename)
        super(Loger,self).__init__(*args,**kwargs)

    def rotate(self):
        shutil.move(self.fname, self.fname + '.0')

    def run(self):
        while True:

            with open(self.fname, 'a') as f:
                while True:
                    dt = random.uniform(10, 20)
                    # build_id = uuid.uuid1()
                    build_id = id_generator()
                    f.write(log_patern % (build_id, dt))
                    time.sleep(dt/2)
                    if os.path.getsize(self.fname) > 100*1024*1024:
                        break
            self.rotate()


def httpserver(server_class=BaseHTTPServer.HTTPServer,
        handler_class=SimpleHTTPServer.SimpleHTTPRequestHandler):

    server_address = ('0.0.0.0', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    l = Loger()
    l.start()
    os.chdir(os.path.dirname(l.fname))
    httpserver()
    l.join()

