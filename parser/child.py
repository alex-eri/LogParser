__author__ = 'eri'
import re
import urllib2
import httplib

donetime_re = re.compile('(DoneTime=)(\d+.\d+) DONE')

class Buffer():
    def __init__(self,f):
        self.f = f
        self.buf = ''
        self.cursor = 0

    def readlines(self):
        buf = True
        while buf:
            buf = self.f.read(2048)
            self.cursor += len(buf)
            self.buffer += buf
            while True:
                split = self.buf.split('\n',1)
                self.buf = split[-1]

                if len(split) > 1:
                    yield split[0]
                else:
                    break





class Parser(object):
    def __init__(self,host,queue):
        self.host = host
        self.queue = queue
        self.cursor = 0
        self.size = 0
        self.host = host

    def connect(self):
        self.conn =  httplib.HTTPConnection(self.host)

    def parse(self, response):
        buffer = Buffer(response)
        for line in buffer.readlines():
            m = donetime_re.search(line)
            if m:
                return float(m.group(2))



    def get(self,uri):
        self.conn.request('GET', uri)
        self.conn.putheader('Range','bytes=%d-' % self.cursor)
        self.conn.endheaders()
        res = self.conn.getresponse()
        self.size = res.getheader('content-length')
        result = self.parse(res)
        if result:
            self.queue.put([self.host,result])

    def head(self):
        self.conn.request('HEAD','/log')
        res =  self.conn.getresponse()
        size = res.getheader('content-length')
        if size > self.size:
            self.get('/log')
        elif size < self.size:
            self.get('/log.0')
            self.cursor = 0
            self.get('/log')

    def run(self):
        self.connect()
        while True:
            self.head()

