import time

__author__ = 'eri'

import settings
from multiprocessing import Process, Queue, current_process
from child import Parser



def parser(host,done_queue):
    Parser(host,done_queue).run()


def flush(t,results):
    t = time.strftime("%a, %d %b %Y %H:%M:%S",time.gmtime(t) )
    with open('done.log','a') as log:
        lines = []
        for host in results.keys():
            avg = sum(results[host])/float(len(results[host]))
            lines.append("[%s] [%s]: average=%f \n" % (t,host,avg))
        log.writelines(lines)




def main():
    done_queue = Queue()

    results = {}
    for host in settings.machines:
        results[host] = []
        Process(target=parser,args=(host,done_queue)).start()
    t = time.time()
    while True:
        host,done_time = done_queue.get()
        results[host].append(done_time)
        if time.time() - t > 1 :
            t = time.time()
            flush(t,results)
            for host in results.keys():
                results[host] = []


if __name__ == "__main__":
    main()