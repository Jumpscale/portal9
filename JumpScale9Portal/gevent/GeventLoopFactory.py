from js9 import j

from .GeventLoop import GeventLoop
import time

import gevent
import gevent.subprocess


class GeventLoopFactory:

    # def __init__(self):
    #     self.__jslocation__ = "j.core.gevent"

    def getGeventLoopClass(self):
        return GeventLoop

    def work(self):
        counter = 0
        while True:
            counter += 1
            time.sleep(1)
            print(counter)

    def testMultiProcess(self):

        def count_greenlets(s):
            import gc
            from greenlet import greenlet
            greenlets = [obj for obj in gc.get_objects() if isinstance(obj, greenlet)]
            print('At "%s", greenlets: %d' % (s, len(greenlets)))
            for k in greenlets:
                print('  * %s' % (k,))

        def read_stream(stream):
            try:
                while not stream.closed:
                    l = stream.readline()
                    if not l:
                        break
                    print(l.rstrip())
            except RuntimeError:
                # process was terminated abruptly
                pass

        count_greenlets('start')

        processes = {}
        for i in range(50):
            p = gevent.subprocess.Popen('python3', stdout=gevent.subprocess.PIPE,
                                        stderr=gevent.subprocess.PIPE, stdin=gevent.subprocess.PIPE, shell=True)
            processes[i] = (p,
                            gevent.spawn(read_stream, p.stdout),
                            gevent.spawn(read_stream, p.stderr)
                            )

            p.stdin.write(b"from js9 import j\nj.core.gevent.work()\n")
            p.stdin.close()
            print(1)

        count_greenlets('after p1')

        p.wait()
