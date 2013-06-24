__author__ = 'eri'

import settings
from multiprocessing import Process, Queue, current_process

def parser(host,done_queue):
    pass


def

def main():
    done_queue = Queue()
    results = {}
    for host in settings.machines:
        results[host] = []
        Process(target=parser,args=(host,done_queue)).start()

    while True:
        host,done_time = done_queue.get()
        results[host].append(done_time)
